from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product, Variation
from .models import Cart, CartItem

# getting id from the session
def _cart_id(request):
    cart = request.session.session_key
    # create a new session if no session
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #gets the specifice product when a id of that product is passed when calling it
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        #create a new cart
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cartItem_exists = CartItem.objects.filter(product = product, cart = cart).exists()

    if is_cartItem_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart) #filtered product and cart that we wrote the function for is passed as argument
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variation  = item.variation.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)

        print(existing_variation_list)
        if product_variation in existing_variation_list : 
            index = existing_variation_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id = item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if(len(product_variation) > 0): 
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save() 
    return redirect('cart')

def decrement_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try :
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete() # delete if item is only one
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)  