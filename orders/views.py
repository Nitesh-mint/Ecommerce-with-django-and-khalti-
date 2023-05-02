from django.shortcuts import render
from carts.models import CartItem
from django.shortcuts import redirect
from .forms import orderForm

from .models import Order
from django.http import HttpResponse
import datetime

def payment(request):
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
            print(is_payment_made)
            is_payment_made = request.POST.get('p')
            print(is_payment_made)

            return render(request, 'orders/payment.html', context)
        else:
            return HttpResponse(form.fields)
        
    else:
        return redirect('checkout')
        


