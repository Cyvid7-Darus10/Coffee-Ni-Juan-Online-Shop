from math import ceil
from django.shortcuts import render
from product.models import Product
from .models import Order
from django.http import HttpResponse

# global variables for js and css
js = []
css = []

# helper function
def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
    return obj

def shopping_cart(request):

    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js
    })

def check_out(request):
    order = get_if_exists(Product, **{'id':id})
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "order" : order
    })