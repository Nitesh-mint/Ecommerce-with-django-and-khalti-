from django.db import models
from category.models import Category
from django.urls import reverse
from django.db.models import Avg

from accounts.models import Account
from datetime import datetime, timedelta

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(max_length=500, blank=True)
    Image = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # to get the specific product url inside the specific category
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    # calculating the average rating of the product
    def averageRating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def reveiewCount(self):
        reviews = ReviewRating.objects.filter(product=self, status=True)
        i = 0
        for review in reviews:
            i = i+1
        return i


class OfferProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    end_date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        today = datetime.today()
        self.end_date = today + timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name
    
    def price_after_discount(self):
        return self.product.price - self.price
    
    def discount_percent(self):
        return round((self.price * 100)/ self.product.price)
    

variation_category_choices = (
    ('color', 'color'),
    ('size','size'),
    ('ram', 'ram'),
    ('storage', 'storage')
)

class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
    def ram(self):
        return super(VariationManager, self).filter(variation_category='ram', is_active=True)
    
    def storage(self):
        return super(VariationManager, self).filter(variation_category='storage', is_active=True)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager() #calling the above method 

    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user  = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE) 
    image  = models.ImageField(upload_to='store/products', max_length=255)


    def __str__(self):
        return self.product.product_name
    

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
 