from math import ceil
from django.shortcuts import render
from .models import Product

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