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

def product_detail(request, category_slug, product_slug):
    try:
        # category ko slug ma category_slug ko value pass huncha and product ko slug ma product_slug pass huncha ra item return huncha
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)
