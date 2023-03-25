from django.shortcuts import render
from . import forms

def registration(request):
    form = forms.RegistrationForm()
    context =  {
        'form': form,
    }
    return render(request,'accounts/registration.html', context)

def login(request):
    return render(request,'accounts/login.html')

def logout(request):
    return 