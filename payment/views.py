from django.shortcuts import render

from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart


from django.http import JsonResponse

from django.core.mail import send_mail

from django.conf import settings

def checkout(request):

# Users with accounts -- pre fill the form

    if request.user.is_authenticated:

        try:

            # Authenticated users WITH shipping information 

            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping': shipping_address}

            


            return render(request, 'payment/checkout.html', context=context)


        except:

            # Authenticated users with NO shipping information

            return render(request, 'payment/checkout.html')
        
    else: 
       
    # guest users

        return render (request, 'payment/checkout.html')
    



















def payment_success(request):

    # Clear shopping cart

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]
    
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    
    return render(request, 'payment/payment-failed.html')



def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # All-in-one shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" +
                            city + "\n" + state + "\n" + zipcode)

        # Shopping cart information 
        cart = Cart(request)

        # Get the total price of items
        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                         amount_paid=total_cost, user=request.user)
        else:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                         amount_paid=total_cost)

        order_id = order.pk

        product_list = []
        for item in cart:
            if request.user.is_authenticated:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                         price=item['price'], user=request.user)
            else:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                         price=item['price'])
            product_list.append(item['product'])

        all_products = product_list

        # Email to customer - This should be outside the if-else block
        customer_email_subject = 'Order received'
        customer_email_body = 'Hi!\n\nThank you for placing your order\n\n' + \
                              'Please see your order below:\n\n' + str(all_products) + '\n\n' + \
                              f'Total paid: £{cart.get_total()}'
        send_mail(customer_email_subject, customer_email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        # Email to the host - This should also be outside the if-else block at the same indentation level as customer email
        host_email_subject = 'New Order Placed'
        host_email_body = f'New order from {name}\n\n' \
                          f'Order ID: {order_id}\n\n' \
                          f'Products: {str(all_products)}\n\n' \
                          f'Total Paid: £{total_cost}'
        try:
            send_mail(host_email_subject, host_email_body, settings.EMAIL_HOST_USER, [settings.HOST_EMAIL], fail_silently=False)
        except Exception as e:
            print(f"Failed to send host email: {e}")

        order_success = True
        response = JsonResponse({'success': order_success})
        return response
                                            
                                            


          




