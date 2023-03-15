from django.shortcuts import render

from carts.models import CartItem
from store.models import Product
from carts.views import _cart_id


def home(request):
    products = Product.objects.all().filter(is_available=True)
    # single_product = 
    # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=)
    context = {
        'products' : products,
    }
    return render(request, 'home.html', context)