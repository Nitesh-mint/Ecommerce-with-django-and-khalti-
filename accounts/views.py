from django.shortcuts import render, redirect
from . import forms
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
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
            messages.success(request, 'Registraion Successful.')
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
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            # messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

#adding this decorator makes sure that a user cannot click logout unless they are logged in
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')