from math import ceil
from django.shortcuts import render
from product.models import Product
from django.http import HttpResponse

# global variables for js and css
js = []
css = []

def shopping_cart(request):

    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js
    })

def check_out(request):

    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js
    })