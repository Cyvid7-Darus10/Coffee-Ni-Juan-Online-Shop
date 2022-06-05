from math import ceil
from django.shortcuts import render,redirect
from payment.models import Order, OrderItem, ShoppingCart, ShoppingCartItem, Payment
from django.http import HttpResponse
from product.models import Product
from product.views import product_item


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

def shopping_cart(request):
    # cart = get_if_exists(ShoppingCart, **{'customer':request.user})
    cart = get_if_exists(ShoppingCart, customer = request.user.id)

    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    
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

def order(request):
    orders = Order.objects.filter(customer=request.user.id)
    order_cnt = len(orders)
    return render(request, "payment/order.html", {
        "csss" : css,
        "jss"  : js,
        "orders" : orders,
        "order_cnt" : order_cnt
    })

def check_out(request):
    cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})

    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "cart" : cart,
    })

def add_order(request, payment):
    customer = request.user
    cart = get_if_exists(ShoppingCart, **{'customer':request.user})
    new_order = Order(customer=customer, payment=payment, status="Ongoing")
    new_order.save()

    products = cart.products()
    for product in products:
        if(product.status == "Selected"):
            new_order_item = OrderItem(order=new_order, product=product.product, quantity=product.quantity, status="Ongoing")
            new_order_item.save()

    shipping_fee = get_if_exists(Product, **{'label':"Shipping Fee"})
    if(payment.payment_option == "cod"):
        new_order_item = OrderItem(order=new_order, product=shipping_fee, quantity=1, status="Ongoing")
        new_order_item.save()

    return home(request)

def add_payment(request, cart):
    if request.POST.get('action') == 'ADD PAYMENT':
        customer = request.user
        address = request.POST['address']
        mobile_number = request.POST['mobile_number']
        total = float(request.POST['total'])
        
        if( request.POST['proof_exist'] == "None"):
            proof ="None"
        else:
            proof = request.FILES['proof']

        payment_option = request.POST['payment_option_input']
        new_payment = Payment(customer=customer, address=address, mobile_number=mobile_number, total=total, payment_option=payment_option, proof=proof)
        
        new_payment.save()
        add_order(request, new_payment)
    return home(request)

def add_cart(request, id):
    # Check if the param action value is ADD TO CART

    cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})    
    # Check if the product is already in the cart
    if cart is None:
        cart = ShoppingCart.objects.create(customer=request.user)

    if request.POST.get('action') == 'ADD TO CART':
        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product})
        if item is None:
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product)

        # get the quantity parameter
        quantity = int(request.POST.get('quantity'))
        item.quantity += quantity
        item.status = "Pending"
        item.save()

    elif request.POST.get('action') == 'BUY NOW':
        for product in cart.products():
            if product.status == "Selected":
                product.status = "Pending"
                product.save()

        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product})
        if item is None:
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product)
        
        quantity = int(request.POST.get('quantity'))
        item.quantity = quantity
        item.status = "Selected"
        item.save()

        return check_out(request, cart.id)

    # redirect to product item page
    return product_item(request, id)

def update_item(request,id):
    item = ShoppingCartItem.objects.get(id=id)

    # get the quantity parameter
    number = 'quantity' + " " +  str(id)
    quantity = request.POST.get(number)
    item.quantity = quantity
    item.save()
    return shopping_cart(request)
    

def remove_cart(request, id):
    item = ShoppingCartItem.objects.filter(id=id)
    item.delete()
    return shopping_cart(request)


def delete_cart(request):
    ShoppingCart.objects.all().delete()
    return shopping_cart(request)

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

