from math import ceil
from django.shortcuts import render,redirect
from payment.models import Order, ShoppingCart, ShoppingCartItem
from django.http import HttpResponse
from product.models import Product
from product.views import product_item

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
    # cart = get_if_exists(ShoppingCart, **{'customer':request.user})
    cart = get_if_exists(ShoppingCart, customer = request.user)
    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user})
    if shopping_cart:
        # get the shopping cart items of the user
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
        item_cnt = len(shopping_cart_items)
    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js,
        "cart": cart,
        "item_cnt" : item_cnt
    })


def check_out(request, id):
    order = get_if_exists(Order, **{'id':id})
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "order" : order
    })


def add_cart(request, id):
    # Check if the param action value is ADD TO CART
    if request.POST.get('action') == 'ADD TO CART':
        # Check if the product is already in the cart
        cart = get_if_exists(ShoppingCart, **{'customer':request.user})
        if cart is None:
            cart = ShoppingCart.objects.create(customer=request.user)
        
        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product})
        if item is None:
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product)

        # get the quantity parameter
        quantity = int(request.POST.get('quantity'))
        item.quantity += quantity
        item.save()

    elif request.POST.get('action') == 'BUY NOW':
        # redirect to buy now
        pass

    # redirect to product item page
    return product_item(request, id)



def remove_cart(request, id):
    # Check if the product is already in the cart
    
    product = get_if_exists(Product, **{'id':id})  
    # item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product})
    # item.delete()
    item = ShoppingCartItem.objects.filter(product=product)
    item.delete()

    #redirect to shopping cart page
    return shopping_cart(request)


def delete_cart(request):
    ShoppingCart.objects.all().delete()
    return shopping_cart(request)