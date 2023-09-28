from django.shortcuts import render, redirect , get_object_or_404  
from .models import Product, ReviewRating, ProductGallery
from category.models import Category 
from carts.models import CartItem
from carts.views import _cart_id
from orders.models import OrderProduct
from accounts.models import UserProfile

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q #to make OR operator possible in searching product in line 57

from django.contrib import messages

from django.http import HttpResponse
from .forms import ReviewForm

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        #category = categories chai hamro prodcut model ma category bhanne variable cha tesma tiyo value pass huncha
        products = Product.objects.all().filter(category=categories, is_available=True)[:4]
        try:
            sort_by = request.GET.get('sort')
            if sort_by == "l2h":    
                products = products.order_by("price")
            elif sort_by == "h2l":
                products = products.order_by("-price")
            elif sort_by == "latest":
                products = products.order_by("-id")
        except:
            pass
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')[:4]
        try:
            sort_by = request.GET.get('sort')
            print(sort_by)
            if sort_by == "l2h":    
                products = products.order_by("price")
            elif sort_by == "h2l":
                products = products.order_by("-price")
            elif sort_by == "latest":
                products = products.order_by("-id")
        except:
            pass
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count  = products.count()
    context = {
            'products': paged_products,
            'product_count' : product_count,
        }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # category ko slug ma category_slug ko value pass huncha and product ko slug ma product_slug pass huncha ra item return huncha
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        reviews = ReviewRating.objects.filter(product__id=single_product.id)
        userprofile = UserProfile.objects.all()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'reviews': reviews,
        'orderproduct':orderproduct,
        'userprofile': userprofile,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = None
    product_count = 0
    keyword = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword), is_available=True)
            product_count = products.count()
            try:
                sort_by = request.GET.get('sort')
                if sort_by == "l2h":    
                    products = products.order_by("price")
                elif sort_by == "h2l":
                    products = products.order_by("-price")
                elif sort_by == "latest":
                    products = products.order_by("-id")
            except:
                pass
        else:
            pass
    context = {
        'products' : products,
        'product_count': product_count,
        'keyword': keyword,
    } 

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews) #instance checks if there is already a review of this product
            form.save()
            messages.success(request, "Thank you for updating the review.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you for your Review.")
                return redirect(url)
