from math import ceil
from django.shortcuts import render,redirect
from .models import Order, OrderItem, ShoppingCart, ShoppingCartItem,Payment
from django.http import HttpResponse
from product.models import Product
from product.views import product_item
from product.views import product_list
from account.views import home
from account.models import Account
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
   
    if request.user.is_authenticated == False: 
        return home(request)
    username = request.user.username
    name = request.user.first_name
    surname = request.user.last_name
    # cart = get_if_exists(ShoppingCart, **{'customer':request.user})
    cart = get_if_exists(ShoppingCart, customer = request.user.id)
    if cart is None:
        cart = ShoppingCart.objects.create(customer=request.user)
    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    item_cnt = shopping_cart.countNotDeletedProducts()
    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js,
        "username":username,
        "name":name,
        "surname": surname,
        "cart": cart,
        "item_cnt" : item_cnt
    })

def check_out(request):
    username = request.user.username
    name = request.user.first_name
    surname = request.user.last_name
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})

    item_cnt = 0
    if request.method == 'POST':
        if request.POST.get('action') == 'Check_out':
            if request.POST.get('selectAll') == 'selectAll':
                ShoppingCartItem.objects.filter(shopping_cart=shopping_cart, status="Pending").update(status="Selected")
            else:
                array = request.POST.getlist("checkItem")
                for i in array:
                     ShoppingCartItem.objects.filter(id=i).update(status="Selected")
        # elif request.POST.get('action') == 'Update Cart':
        #     request.POST.get('quantity')   
        else:
           return delete_cart(request)
   
    if shopping_cart:
        # get the shopping cart items of the user
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart, status="Pending")
        item_cnt = len(shopping_cart_items)
            
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "username":username,
        "name":name,
        "surname": surname,
        "cart" : shopping_cart,
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
            ShoppingCartItem.objects.filter(status="Selected").update(status="Ongoing")

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
    if request.user.is_authenticated == False: 
        return home(request)
        
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
        # for product in cart.products():
        #     if product.status == "Selected":
        #         product.status = "Pending"
        #         product.save()

        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product})
        if item is None:
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product)
        
        quantity = int(request.POST.get('quantity'))
        item.quantity = quantity
        item.status = "Selected"
        item.save()

        return check_out(request)

    # redirect to product item page
    return product_list(request)

def update_item(request,id):
    item = ShoppingCartItem.objects.get(id=id)
    # if request.POST.get('action') == id:
    #     if request.POST.get('checkItem') == id:
    #         ShoppingCartItem.objects.filter(id=id).update(status="Checked")
    if request.POST.get('action') == 'Update Cart':
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
    checkbox = request.POST.get('selectAll')
    if checkbox == 'selectAll':
        ShoppingCartItem.objects.filter(status="Pending").delete()
    return shopping_cart(request)