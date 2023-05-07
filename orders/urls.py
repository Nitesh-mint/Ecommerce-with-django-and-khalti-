from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.placeOrder,name='place_order'),
    path('payment/',views.payment, name='payment'),
    path('ordercomplete/', views.order_complete, name='order_complete')
]