from django import forms
from .models import Order
from accounts.models import DeliveryAddress


class orderForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.CharField(attrs={}))
    class Meta:
        model = Order
        fields= ['first_name','last_name','phone','email','state','area','address']

class DeliveryForm(forms.ModelForm):
    state = forms.CharField(widget=forms.TextInput(attrs={ #attrs in for the css class
        'placeholder': "",
        'class': 'form-control'
    }))
    area = forms.CharField(widget=forms.TextInput(attrs={ #attrs in for the css class
        'placeholder': "",
        'class': 'form-control'
    }))
    class Meta:
        model = DeliveryAddress
        fields = ['state','area']