from django.shortcuts import render

js = []
css = []

def productList(request):
    return render(request, "product/productList.html", {
        "csss" : css,
        "jss"  : js
    })
# Create your views here.

js = []
css = []

def index(request):
    return render(request, "product/product.html", {
        "csss" : css,
        "jss"  : js
    })
