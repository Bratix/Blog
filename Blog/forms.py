from cProfile import label
import email
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    

    class Meta:
        model = User
        fields = ['username','email','password']