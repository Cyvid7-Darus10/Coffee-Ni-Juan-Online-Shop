from django.shortcuts import render
from .forms import productOrder

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
    form = productOrder()
    return render(request, "product/product.html", {
        "csss" : css,
        "jss"  : js,
        "form" : form
    })

# def record_like_view(request, pk):
#     if request.method == 'POST':
#         post = Post.objects.get(pk=pk)
#         post.amount += 1
#         post.save()