from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from . import forms
from .forms import RegistrationForm, UserForm, UserProfileForm, DeliveryForm
from .models import Account, UserProfile, DeliveryAddress
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#for password reset
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#for saving cart items after user logs in 
from carts.views import _cart_id
from carts.models import Cart, CartItem

from orders.models import Order

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = request.POST['country']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            if len(password) >=8:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.phone_number = phone_number
                user.country = country
                messages.success(request, 'Registraion Successful.')
                user.save()
            else:
                messages.error(request, "Password must be 8 or more digits")
                return redirect('register')

        else:
            messages.error(request,form.errors)
            return redirect('register')
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)
                    #get product variation from the cart_id
                    product_variation =[]
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))
                    
                    #getting the product variation from the logged in user if there is any 
                    cart_item = CartItem.objects.filter(user=user)
                    ex_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_variation_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_variation_list:
                            index = ex_variation_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            # messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')
    return render(request,'accounts/login.html')

#adding this decorator makes sure that a user cannot click logout unless they are logged in
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    orders = Order.objects.order_by('-created_at').filter(user__id=request.user.id, is_ordered=True) 
    orders_count = orders.count()
    if UserProfile.objects.filter(user=user).exists():
        userprofile = UserProfile.objects.get(user=user)
        redirect('dashboard')
    else:
        userprofile = UserProfile.objects.create(user=user)
    context = {
        'user': user,
        'orders_count' : orders_count,
        "userprofile":userprofile,
    }
    return render(request,'accounts/dashboard.html',context)

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            #using case sensitive filter
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email], from_email="Hamrodokan@ilam.com")
            send_email.content_subtype = 'html'
            send_email.send()

            messages.success(request, "Password reset email has been sent to your email address, Please check your mail to continue")
            redirect('login')


        else :
            messages.error(request, "No account linked with this email.")
            return redirect('forgotPassword')
        
    return render(request, 'accounts/forgotPassword.html')

def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password.")
        return redirect("resetPassword")
    else:
        messages.error(request, "The link has been expired.")
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password == confirmPassword:
            if len(password) >=8:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfull')
                return redirect('login')
            else:
                messages.error(request, 'Password must be 8 digits or more.')
                return redirect('resetPassword')

        else:
            messages.error(request, 'Password doesnot match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
    
@login_required(login_url='login')
def myOrders(request):
    orderproduct = Order.objects.order_by('-created_at').filter(user=request.user, is_ordered=True)
    context = {
        "orderproduct" : orderproduct,
    }
    return render(request, 'accounts/my_orders.html', context)
@login_required(login_url='login')
def editProfile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user) #gets the userprofile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user) #instance because we want to edit form
        profile_form = UserProfileForm(request.POST,request.FILES, instance=userprofile) #file upload request.FILES
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated")
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)
    
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpass']
        new_password = request.POST['newpass']
        confirm_password = request.POST['confirmpass']
    
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
                success = user.check_password(current_password)
                if success:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,"Password updated successfully")
                else:
                    messages.error(request, "Incorrect current password ")
        else:
            messages.error(request, "Password doesn't match")
    return render(request, 'accounts/change_password.html')


def editDeliveryAddress(request):
    if DeliveryAddress.objects.filter(user=request.user).exists():
        if request.method == "POST":
                print("Nice")
                form = DeliveryForm(request.POST, instance=DeliveryAddress.objects.get(user=request.user))
                form.save()
                messages.success(request, "Address is updated")
        else:
            form = DeliveryForm(instance=request.user)
    else:
        if request.method == "POST":
            form = DeliveryForm(request.POST)
            if form.is_valid():
                data = DeliveryAddress()
                data.state = form.cleaned_data['state']
                data.area = form.cleaned_data['area']
                data.user = request.user
                data.save()
                messages.success(request, "Address has been stored succesfully")
        else:
            form = DeliveryForm()
    return render(request, 'accounts/add_address.html', {'form':form})