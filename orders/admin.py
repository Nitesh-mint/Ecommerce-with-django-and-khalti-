from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity','product_price')
    extra = 0 

class orderAdmin(admin.ModelAdmin):
    list_display  = ['order_number','full_name', 'phone', 'email', 'state', 'grand_total', 'tax', 'status', 'is_ordered',  'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 15
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order, orderAdmin)
admin.site.register(OrderProduct)