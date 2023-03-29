from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registration/", views.registration, name="register"),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("", views.dashboard, name='dashboard'),
    path("forgotPassword/",views.forgotPassword, name='forgotPassword'),
    path("resetPassword_validate/<uidb64>/<token>/",views.resetPassword_validate, name='resetPassword_validate'),
]