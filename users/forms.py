from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = ("email", "password1", 'password2')


class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
