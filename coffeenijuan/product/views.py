from math import ceil
from django.shortcuts import render
from .models import Product
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


def product_list(request):
    # check if there is post request
    if request.method == "POST":
        # use the filter data to get the product list
        max = request.POST.get('max', None)
        max = max if max else 1000.00
        min = request.POST.get('min', 0)
        min = min if min else 0.00
        rating = request.POST.get('rating', 0)
        rating = rating if rating else 0.00

        products = Product.objects.filter(price__gte=min, price__lte=max, rating__gte=rating)
    else:
        # get all products
        products = Product.objects.all()

    return render(request, "product/product_list.html", {
        "csss" : css,
        "jss"  : js,
        "products" : products
    })

def product_item(request, id):
    product = get_if_exists(Product, **{'id':id})
    
    rating = product.rating
    if not rating:
        rating = 0
    not_whole = rating % 1
    rating = int(rating)

    return render(request, "product/product_item.html", {
        "csss"     : css,
        "jss"      : js,
        "product"  : product,
        "n"        : range(rating),
        "n2"       : range(5 - (rating + (1 if not_whole else 0))),
        'not_whole': not_whole
    })