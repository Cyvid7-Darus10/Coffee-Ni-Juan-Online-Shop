from django.shortcuts import render

# Create your views here.

js = []
css = []

def product(request):
    return render(request, "product/product.html", {
        "csss" : css,
        "jss"  : js
    })