import logging
from decimal import Decimal
from django.db import transaction
from django.contrib.sessions.models import Session
from store.models import Product
from .models import CartItem
from datetime import datetime, timedelta  # Added for expire_date

logger = logging.getLogger(__name__)

class Cart:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session = request.session
        # Ensure session key exists—Django creates it automatically
        if not self.session.session_key:
            self.session.save()  # Forces session creation with expire_date
        self.session_key = self.session.session_key

    def get_cart_items(self):
        if self.user:
            return CartItem.objects.filter(user=self.user)
        return CartItem.objects.filter(session_key=self.session_key)

    @transaction.atomic
    def add(self, product, product_qty):
        product_id = str(product.id)
        logger.debug(f"Adding product {product_id}: requested qty={product_qty}, current stock={product.quantity}")
        
        if product.quantity < product_qty:
            logger.error(f"Not enough stock. Requested: {product_qty}, Available: {product.quantity}")
            raise ValueError(f"Not enough stock. Requested: {product_qty}, Available: {product.quantity}")

        cart_item, created = CartItem.objects.get_or_create(
            user=self.user if self.user else None,
            session_key=self.session_key if not self.user else None,
            product=product,
            defaults={'quantity': product_qty}
        )
        if not created:
            cart_item.quantity += product_qty

        product.quantity -= product_qty
        product.save()
        cart_item.save()
        logger.debug(f"Stock after add: {product.quantity}, Cart qty: {cart_item.quantity}")

    @transaction.atomic
    def update(self, product, qty):
        product_id = str(product.id)
        logger.debug(f"Starting update for product {product_id}: requested new_qty={qty}")
        
        product = Product.objects.select_for_update().get(id=product_id)
        cart_items = self.get_cart_items().select_for_update()
        
        try:
            cart_item = cart_items.get(product=product)
            old_qty = cart_item.quantity
            stock_change = qty - old_qty
            new_stock = product.quantity - stock_change
            
            logger.debug(f"Old qty={old_qty}, New qty={qty}, Stock change={stock_change}, Current stock={product.quantity}, Calculated new_stock={new_stock}")
            if new_stock < 0:
                logger.error(f"Blocked: Not enough stock. Required change: {stock_change}, Available: {product.quantity}")
                raise ValueError(f"Not enough stock. Required change: {stock_change}, Available: {product.quantity}")
            
            product.quantity = new_stock
            product.save()
            cart_item.quantity = qty
            cart_item.save()
            logger.debug(f"Stock after update: {product.quantity}, Cart qty: {cart_item.quantity}")
        except CartItem.DoesNotExist:
            logger.error(f"Product {product_id} not in cart")
            raise ValueError("Product not in cart")

    @transaction.atomic
    def delete(self, product):
        product_id = str(product.id)
        logger.debug(f"Deleting product {product_id}")
        try:
            cart_item = self.get_cart_items().get(product=product)
            qty_to_return = cart_item.quantity
            product.quantity += qty_to_return
            product.save()
            cart_item.delete()
            logger.debug(f"Deleted product {product_id}: Returned {qty_to_return}, New stock={product.quantity}")
        except CartItem.DoesNotExist:
            logger.debug(f"Product {product_id} not found for deletion")

    @transaction.atomic
    def clear(self, restore_stock=True):
        cart_items = self.get_cart_items()
        for item in cart_items:
            if restore_stock:
                item.product.quantity += item.quantity
                item.product.save()
                logger.debug(f"Clearing cart: Returned {item.quantity} to product {item.product.id}, New stock={item.product.quantity}")
            else:
                logger.debug(f"Clearing cart: Kept stock at {item.product.quantity} for product {item.product.id}, qty {item.quantity} removed")
        cart_items.delete()

    def __len__(self):
        return sum(item.quantity for item in self.get_cart_items())

    def __iter__(self):
        cart_items = self.get_cart_items().select_related('product')
        for item in cart_items:
            yield {
                'product': item.product,
                'qty': item.quantity,
                'price': Decimal(str(item.product.price)),
                'total': Decimal(str(item.product.price)) * item.quantity
            }

    def get_total(self):
        return sum(Decimal(str(item.product.price)) * item.quantity for item in self.get_cart_items())