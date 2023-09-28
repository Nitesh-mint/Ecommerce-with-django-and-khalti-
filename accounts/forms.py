from django import forms
from .models import Account, UserProfile, DeliveryAddress

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ #attrs in for the css class
        'placeholder': "",
        'class': 'form-control'
    }))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "",
        'class': 'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','email', 'phone_number', 'country']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = ""
        self.fields['last_name'].widget.attrs['placeholder'] = ""
        self.fields['email'].widget.attrs['placeholder'] = ""
        self.fields['phone_number'].widget.attrs['placeholder'] = ""

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
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name', 'phone_number','email']
    

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter your first name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter your last name"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter your phone number"

        # to add boostrap class to all the fields in the registraion page
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['state','area','address','profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['placeholder'] = "Enter your distric name"
        self.fields['area'].widget.attrs['placeholder'] = "Enter your area name"
        self.fields['address'].widget.attrs['placeholder'] = "Enter your full address"

        # to add boostrap class to all the fields in the registraion page
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    

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