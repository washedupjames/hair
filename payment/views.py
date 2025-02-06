from django.shortcuts import render, redirect
from cart.cart import Cart
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django_countries.fields import CountryField
from django.db import transaction
from payment.models import Order, OrderItem
from payment.models import ShippingAddress
from django.contrib.auth.models import AnonymousUser

def checkout(request):
    # Define cart at the start of the function
    cart = Cart(request)
    subtotal = cart.get_total()

    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        shipping = None  # For guest users, no shipping address from database
    else:
        try:
            shipping = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping = None  # Handle case where user is logged in but has no shipping address

    context = {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,  
        'SANDBOX_PAYPAL_CLIENT_ID': settings.SANDBOX_PAYPAL_CLIENT_ID, 
        'shipping_cost': '£0.00',
        'total_cost': None,
        'cart_total': subtotal,
        'COUNTRY_CHOICES': list(CountryField().choices),
        'shipping': shipping 
    }
    
    return render(request, 'payment/checkout.html', context=context)


def payment_success(request):
    # Clear shopping cart
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

@transaction.atomic
def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')

        shipping_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}\n{country}"

        cart = Cart(request)
        cart_total = cart.get_total() 

        # Calculate shipping cost
        domesticRate = Decimal('3.00')  # UK shipping rate
        internationalRate = Decimal('5.00')  # International shipping rate
        shipping_cost = domesticRate if country == 'GB' else internationalRate

        # Calculate total cost including shipping
        total_cost = cart_total + shipping_cost

        # Create order for both authenticated and guest users
        order = None
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name, 
                email=email, 
                shipping_address=shipping_address,
                amount_paid=total_cost, 
                user=request.user
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order, 
                    product=item['product'], 
                    quantity=item['qty'],
                    price=item['price'], 
                    user=request.user
                )
        else:
            order = Order.objects.create(
                full_name=name, 
                email=email, 
                shipping_address=shipping_address,
                amount_paid=total_cost
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order, 
                    product=item['product'], 
                    quantity=item['qty'],
                    price=item['price']
                )

        # Convert cart to a readable string for emails
        cart_items = '\n'.join([f"- {item['product'].title} x {item['qty']} - £{item['price']}" for item in cart])

        # Email to customer
        customer_email_subject = 'Order received'
        customer_email_body = f'''Hi!

Thank you for placing your order

Please see your order below:

{cart_items}

Cart: £{cart_total}
Shipping: £{shipping_cost}

Total: £{total_cost}'''
        send_mail(customer_email_subject, customer_email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        # Email to the host
        host_email_subject = 'New Order Placed'
        host_email_body = f'''New order from {name}

Address: 
{shipping_address}

Products:
{cart_items}

Cart: £{cart_total}
Shipping: £{shipping_cost}

Total: £{total_cost}'''
        
        try:
            send_mail(host_email_subject, host_email_body, settings.EMAIL_HOST_USER, [settings.HOST_EMAIL], fail_silently=False)
        except Exception as e:
            print(f"Failed to send host email: {e}")

        # Clear cart after order completion
        cart.clear()

        order_success = True
        response = JsonResponse({'success': order_success, 'newCartQty': 0})
        return response