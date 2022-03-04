from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Valid Email Required')

    class Meta:
        model = Account
        fields = ('email', 'username', 'pwd1', 'pwd2')


