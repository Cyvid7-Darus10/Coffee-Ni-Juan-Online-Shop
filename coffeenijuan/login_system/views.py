from django.shortcuts import render
from django.http import HttpResponseRedirect

js = []
css = []

def home(request):
    return render(request, "login_system/home.html", {
        "csss" : css,
        "jss"  : js
    })