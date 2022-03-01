from django.shortcuts import render
from django.http import HttpResponseRedirect

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