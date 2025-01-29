from django.shortcuts import render
from cart.cart import Cart
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django_countries.fields import CountryField

from django.shortcuts import render
from cart.cart import Cart
from django_countries.fields import CountryField
import os

def checkout(request):
    cart = Cart(request)
    subtotal = cart.get_total()
    
    context = {
        'PAYPAL_CLIENT_ID': os.getenv('PAYPAL_CLIENT_ID'),
        'shipping_cost': '£0.00',
        'total_cost': None,
        'cart_total': subtotal,
        'COUNTRY_CHOICES': list(CountryField().choices)
    }
    
    return render(request, 'payment/checkout.html', context=context)

def payment_success(request):
    # Clear shopping cart
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def complete_order(request):
    if request.POST.get('action') == 'post':
        # Here you would process the form data, but we're focusing on the checkout process
        # so we'll keep this simple for now
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')

        # All-in-one shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" +
                            city + "\n" + state + "\n" + zipcode + "\n" + country)

        # Shopping cart information 
        cart = Cart(request)

        # Get the total price of items
        total_cost = cart.get_total()

        # Here you would typically save this information or process it further

        # Email to customer
        customer_email_subject = 'Order received'
        customer_email_body = 'Hi!\n\nThank you for placing your order\n\n' + \
                              'Please see your order below:\n\n' + str(cart) + '\n\n' + \
                              f'Total paid: £{total_cost}'
        send_mail(customer_email_subject, customer_email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        # Email to the host
        host_email_subject = 'New Order Placed'
        host_email_body = f'New order from {name}\n\n' \
                          f'Address: {shipping_address}\n\n' \
                          f'Products: {str(cart)}\n\n' \
                          f'Total Paid: £{total_cost}'
        try:
            send_mail(host_email_subject, host_email_body, settings.EMAIL_HOST_USER, [settings.HOST_EMAIL], fail_silently=False)
        except Exception as e:
            print(f"Failed to send host email: {e}")

        order_success = True
        response = JsonResponse({'success': order_success})
        return response