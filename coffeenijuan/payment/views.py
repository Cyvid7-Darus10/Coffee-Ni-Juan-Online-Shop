from math import ceil
from django.shortcuts import render
from payment.models import Order, ShoppingCart, ShoppingCartItem
from django.http import HttpResponse
from payment.forms import OrderForm

# global variables for js and css
js = []
css = []

# def createpost(request):
#         if request.method == 'POST':
#             if request.POST.get('title') and request.POST.get('content'):
#                 post=Post()
#                 post.title= request.POST.get('title')
#                 post.content= request.POST.get('content')
#                 post.save()
                
#                 return render(request, 'posts/create.html')  
#         else:
#                 return render(request,'posts/create.html')

# def addOrder(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = Order()
#             order.customer = 

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
    cart = get_if_exists(ShoppingCart, **{'id':id})
    order = get_if_exists(Order, **{'id':id})
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "cart": cart
    })

def product_item(request, id):
    product = get_if_exists(Product, **{'id':id})

    if not product:
        return redirect('product:product_list')
    
    rating = product.rating
    not_whole = rating % 1
    rating = int(rating)

    return render(request, "product/product_item.html", {
        "csss"        : css,
        "jss"         : js,
        "product"     : product,
        "stars"       : range(rating),
        "empty_stars" : range(5 - (rating + (1 if not_whole else 0))),
        'not_whole'   : not_whole
    })

def home(request):
    page = "home"

    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })