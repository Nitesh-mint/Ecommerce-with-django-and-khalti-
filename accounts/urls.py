from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registration/", views.registration, name="register"),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("forgotPassword/",views.forgotPassword, name='forgotPassword'),
    path("resetPassword_validate/<uidb64>/<token>/",views.resetPassword_validate, name='resetPassword_validate'),
    path("resetPassword/", views.resetPassword, name="resetPassword"),
    path("my_orders/", views.myOrders, name="myOrders"),
    path("editProfile/", views.editProfile, name="editProfile"),
    path("change_password/", views.change_password, name="changepassword"),
    path("edit_address/", views.editDeliveryAddress, name="editAddresss"),
]