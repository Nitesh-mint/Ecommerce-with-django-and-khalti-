from django.contrib import admin

from .models import Product, Variation, ReviewRating, ProductGallery, OfferProducts
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock' , 'category', 'modified_date','is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('is_available','stock','price')
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(OfferProducts)
