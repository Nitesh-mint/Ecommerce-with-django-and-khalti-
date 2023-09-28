from django.shortcuts import render

from carts.models import CartItem
from store.models import Product, OfferProducts
from carts.views import _cart_id

from datetime import datetime
import pytz


def home(request):
    products = Product.objects.all().filter(is_available=True)
    offer_products = OfferProducts.objects.all().filter(is_active=True)
    kathmandu_timezone = pytz.timezone('Asia/Kathmandu')
    current_datetime = datetime.now(tz=kathmandu_timezone)
    for p in offer_products:
        if p.end_date < current_datetime:
            p.is_active = False
            p = p.save()
    context = {
        'products' : products,
        'offer_products' : offer_products,
    }
    return render(request, 'home.html', context)