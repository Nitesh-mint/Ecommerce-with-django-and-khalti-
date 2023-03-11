from django.db import models 
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250,blank=True) #blank says that it can be empty or may be populated
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    # meta class here is to make the typo mistake that djang automaticlally go through
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # to make get link of the product according to the category
    def get_url(self):
        return reverse('product_by_category', args=[self.slug])
 
    def __str__(self):
        return self.category_name