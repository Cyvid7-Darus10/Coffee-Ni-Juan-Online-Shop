from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from account.forms import RegistrationForm

js = []
css = []

def home(request):
    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js
    })

def login(request):
    return render(request, "account/login.html", {
        "csss" : css,
        "jss"  : js
    })

def register(request):
    return render(request, "account/register.html", {
        "csss" : css,
        "jss"  : js
    })