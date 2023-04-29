from django.urls import path
from .views import placeOrder

urlpatterns = [
    path('place_order/',placeOrder,name='place_order'),
]