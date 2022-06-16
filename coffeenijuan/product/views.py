from django.shortcuts import render, redirect
from .models import Product
from payment.models import ShoppingCart
from payment.models import OrderItem
from account.support import get_if_exists

# global variables for js and css
js = []
css = []


# @login_required
def product_list(request):

    rating = 0
    # check if there is post request
    label = request.GET.get('label')
    if label:
        products = Product.objects.filter(label__icontains=label)
    elif request.method == "POST":
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

    if request.POST.get('submit_type') == 'SELECT ALL':
        products = Product.objects.all()
        rating = 0

    all_products = Product.objects.all()
    
    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.count_not_deleted_products()

    return render(request, "product/product_list.html", {
        "csss"         : css,
        "jss"          : js,
        "products"     : products,
        "all_products" : all_products,
        'item_cnt'     : item_cnt,
        "rating"       : rating
    })


def product_item(request, id):
    product = get_if_exists(Product, **{'id':id})

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
        item_cnt = shopping_cart.count_not_deleted_products()

    # get ramdom five products
    random_products = Product.objects.order_by('?')[:4]

    product_orders = OrderItem.objects.filter(product=product.id)
    count_sold = 0
    for p in product_orders:
        if(p.status == "ongoing"):
            count_sold += p.quantity
        if(p.status == "delivered"):
            count_sold += p.quantity

    return render(request, "product/product_item.html", {
        "csss"              : css,
        "jss"               : js,
        "product"           : product,
        "stars"             : range(rating),
        "empty_stars"       : range(5 - (rating + (1 if not_whole else 0))),
        'not_whole'         : not_whole,
        'item_cnt'          : item_cnt,
        "random_products"   : random_products,
        "count_sold"        : count_sold
    })