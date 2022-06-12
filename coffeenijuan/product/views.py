from math import ceil
from django.shortcuts import render, redirect
from .models import Product
from payment.models import ShoppingCart, ShoppingCartItem
from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
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

# @login_required
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
    
    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.countNotDeletedProducts()

    return render(request, "product/product_list.html", {
        "csss"      : css,
        "jss"       : js,
        "products"  : products,
        'item_cnt'  : item_cnt
    })

def product_item(request, id):
   
    product = get_if_exists(Product, **{'id':id})
    # get all products
    items = Product.objects.all()

    if not product:
        return redirect('product:product_list')
    
    rating = product.rating
    if not rating:
        rating = 0
    not_whole = rating % 1
    rating = int(rating)

   # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.countNotDeletedProducts()

    return render(request, "product/product_item.html", {
        "csss"        : css,
        "jss"         : js,
        "product"     : product,
        "stars"       : range(rating),
        "empty_stars" : range(5 - (rating + (1 if not_whole else 0))),
        'not_whole'   : not_whole,
        'item_cnt'    : item_cnt,
        "items" :   items
    })