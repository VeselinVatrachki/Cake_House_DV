from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass