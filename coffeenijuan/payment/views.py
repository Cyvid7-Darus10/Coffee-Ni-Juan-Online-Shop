from math import ceil
from django.shortcuts import render
from payment.models import Order, ShoppingCart, ShoppingCartItem
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

def shopping_cart(request, id):
    cart = get_if_exists(ShoppingCart, **{'id':id})
    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js,
        "cart": cart
    })

def check_out(request, id):
    order = get_if_exists(Order, **{'id':id})
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "order" : order
    })