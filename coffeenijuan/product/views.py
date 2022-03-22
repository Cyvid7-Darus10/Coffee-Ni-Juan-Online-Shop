from django.shortcuts import render

js = []
css = []

def productList(request):
    return render(request, "product/productList.html", {
        "csss" : css,
        "jss"  : js
    })
