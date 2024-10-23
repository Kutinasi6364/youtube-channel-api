from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    class Meta:
        mosel = User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )