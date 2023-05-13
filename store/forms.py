from .models import ReviewRating
from django import forms

class ReviewForm(forms.ModelForm):
    model = ReviewRating
    fields = ['subject','review','rating']
    