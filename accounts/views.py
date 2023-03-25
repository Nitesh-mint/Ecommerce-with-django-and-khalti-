from django.shortcuts import render
from . import forms
from .forms import RegistrationForm
from .models import Account

def registration(request):
    if request.method == 'POST':
        print("Inside firs if ")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("inside second if")
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.object.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.country = country
            user.save()
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context =  {
        'form': form,
    }
    return render(request,'accounts/registration.html', context)

def login(request):
    return render(request,'accounts/login.html')

def logout(request):
    return 