from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity', 1))  # Default to 1 if not provided

            product = get_object_or_404(Product, id=product_id)

            try:
                cart.add(product=product, product_qty=product_quantity)
                cart_quantity = cart.__len__()
                cart_total = cart.get_total()
                response = JsonResponse({
                    'qty': cart_quantity, 
                    'total': cart_total, 
                    'success': True
                })
            except ValueError as e:
                response = JsonResponse({
                    'qty': cart.__len__(), 
                    'total': cart.get_total(), 
                    'success': False, 
                    'message': str(e)
                }, status=400)
        
            return response
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def cart_delete(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            
            cart.delete(product=product)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()
            response = JsonResponse({
                'qty': cart_quantity, 
                'total': cart_total, 
                'success': True
            })
            return response
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def cart_update(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)

            try:
                cart.update(product=product, qty=product_quantity)
                # Refresh product after update to get latest stock
                product = Product.objects.get(id=product_id)
                cart_quantity = cart.__len__()
                cart_total = cart.get_total()
                response = JsonResponse({
                    'qty': cart_quantity,
                    'total': cart_total,
                    'product_id': product_id,
                    'price': float(product.price),
                    'product_quantity': product_quantity,
                    'success': True,
                    'new_stock': product.quantity  # Use refreshed stock
                })
            except ValueError as e:
                response = JsonResponse({
                    'qty': cart.__len__(),
                    'total': cart.get_total(),
                    'success': False,
                    'message': str(e)
                }, status=400)
            
            return response
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)