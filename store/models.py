from django.db import models
from category.models import Category
from django.urls import reverse

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
