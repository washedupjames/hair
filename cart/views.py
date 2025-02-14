from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        # Check if there's enough stock
        if product.quantity >= product_quantity:
            # Reduce the stock
            product.quantity -= product_quantity
            product.save()
            
            cart.add(product=product, product_qty=product_quantity)
            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity, 'success': True})
        else:
            # Not enough stock, inform the user
            response = JsonResponse({'qty': cart_quantity, 'success': False, 'message': 'Not enough stock available.'})

        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        # Check if there's enough stock for the update
        if product.quantity >= product_quantity:
            # Update the stock based on the difference between old and new quantity
            old_quantity = cart.get(product_id).quantity  # Assuming Cart.get() returns an item with 'quantity'
            quantity_diff = product_quantity - old_quantity
            product.quantity -= quantity_diff
            product.save()
            
            cart.update(product=product_id, qty=product_quantity)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()
            response = JsonResponse({'qty': cart_quantity, 'total': cart_total, 'success': True})
        else:
            # Not enough stock to update to the new quantity
            response = JsonResponse({'qty': cart_quantity, 'total': cart_total, 'success': False, 'message': 'Not enough stock available for update.'})

        return response