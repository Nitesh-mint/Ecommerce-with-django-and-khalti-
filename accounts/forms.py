from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ #attrs in for the css class
        'placeholder': "Enter a password",
        'class': 'form-control'
    }))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Confirm your password",
        'class': 'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','email', 'phone_number', 'country']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter your first name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter your last name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter your email"
        self.fields['country'].widget.attrs['placeholder'] = "Enter your country name"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter your phone number"

        # to add boostrap class to all the fields in the registraion page
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm']
        if password != confirm_password:
            raise forms.ValidationError(
                'Password doesnot match'
            )