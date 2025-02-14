from decimal import Decimal
from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def clear(self):
        self.cart = {}
        self.session['session_key'] = {}
        self.session.modified = True

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product.quantity >= product_qty:  # Check stock
            if product_id in self.cart:
                self.cart[product_id]['qty'] = product_qty
            else:
                self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
            # Reduce stock
            product.quantity -= product_qty
            product.save()
        else:
            raise ValueError("Not enough stock available.")
        
        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.cart:
            old_qty = self.cart[product_id]['qty']
            if product.quantity >= qty - old_qty:  # Check if there's enough stock for the change
                product.quantity -= (qty - old_qty)
                product.save()
                self.cart[product_id]['qty'] = qty
            else:
                raise ValueError("Not enough stock to update to this quantity.")
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        import copy
        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())