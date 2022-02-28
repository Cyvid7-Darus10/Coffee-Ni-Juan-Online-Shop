from django.shortcuts import render
from django.http import HttpResponseRedirect

js = []
css = []

def home(request):
    return render(request, "login_system/home.html", {
        "csss" : css,
        "jss"  : js
    })

def login(request):
    return render(request, "login_system/login.html", {
        "csss" : css,
        "jss"  : js
    })

def register(request):
    return render(request, "login_system/register.html", {
        "csss" : css,
        "jss"  : js
    })