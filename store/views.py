from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category 

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        #category = categories chai hamro prodcut model ma category bhanne variable cha tesma tiyo value pass huncha
        products = Product.objects.all().filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count  = products.count()

    context = {
            'products': products,
            'product_count' : product_count,
        }
    return render(request, 'store/store.html', context)