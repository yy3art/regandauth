from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )