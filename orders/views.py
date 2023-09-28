from django.shortcuts import render
from carts.models import CartItem
from django.shortcuts import redirect
from .forms import orderForm

from .models import Order, Payment, OrderProduct
from django.http import HttpResponse
import datetime

from store.models import Product

import json

#for sending mail 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


def payment(request):
    body = json.loads(request.body)
    # getting the order object
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # storing to the payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.grand_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    #move the cart items to the ordered product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity  = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        productvaritaion = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(productvaritaion)
        orderproduct.save()

        #reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock = product.stock - item.quantity
        product.save()

    #delete the products that are ordered
    CartItem.objects.filter(user=request.user).delete()

    #send mail to the user 
    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_received_email.html',{
            'user':request.user,
            'order': order,
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email], from_email="Hamrodokan@ilam.com")
    send_email.content_subtype = 'html'
    send_email.send()
    print("Sent mail success")

    return render(request, 'orders/payment.html')

def placeOrder(request, total=0, quantity=0):
    is_payment_made = False
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <1:
        return redirect('store')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = 0.02 * total
    grand_total = total + tax
    
    if request.method == 'POST':
        form = orderForm(request.POST)
        print(form.errors)
        #saving the data to the models if the form is valid
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.state = form.cleaned_data['state']
            data.area = form.cleaned_data['area']
            data.address = form.cleaned_data['address']
            # data.order_note = form.cleaned_data['order_note']
            data.tax  = tax
            data.grand_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Generating order number 
            year = int(datetime.date.today().strftime('%Y'))
            day  = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            full_date = datetime.date(year,month,day)
            current_date = full_date.strftime('%Y%m%d')
            #now finally order_number is generated with the help of the date
            order_number  = current_date + str(data.id) #here data.id is the primary key of the Order
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'tax': tax,
                'grand_total' : grand_total,
                "is_payment_made" : is_payment_made,
            }

            return render(request, 'orders/payment.html', context)
        else:
            return HttpResponse(form.fields)
        
    else:
        return redirect('checkout')
        
@login_required
def order_complete(request):
    return render(request, 'orders/order_complete.html')
