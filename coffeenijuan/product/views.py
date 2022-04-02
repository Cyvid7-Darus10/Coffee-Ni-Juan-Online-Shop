from django.shortcuts import render
from .forms import productOrder

# global variables for js and css
js = []
css = []

def product_list(request):
    return render(request, "product/product_list.html", {
        "csss" : css,
        "jss"  : js
    })

def product_item(request):
    return render(request, "product/product_item.html", {
        "csss" : css,
        "jss"  : js,
    })