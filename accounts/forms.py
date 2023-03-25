from django.forms import ModelForm
from .models import Account

class RegistrationForm(ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','username','email', 'phone_number']
