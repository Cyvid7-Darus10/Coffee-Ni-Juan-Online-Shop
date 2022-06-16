from django.contrib import messages
from math import ceil
from django.shortcuts import render,redirect
from .models import Order, OrderItem, ShoppingCart, ShoppingCartItem, Payment
from product.models import Product
from account.support import get_if_exists
from django.shortcuts import redirect
from .decorators import users_only

# global variables for js and css
js = []
css = []


@users_only
def shopping_cart(request):
    shopping_cart = get_if_exists(ShoppingCart, customer = request.user.id)
    if shopping_cart is None:
        shopping_cart = ShoppingCart.objects.create(customer=request.user)

    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.count_not_deleted_products()
    return render(request, "payment/shopping_cart.html", {
        "csss"          : css,
        "jss"           : js,
        "shopping_cart" : shopping_cart,
        "item_cnt"      : item_cnt
    })


@users_only
def check_out(request):
    item_cnt = 0
    if request.method == 'POST':
        if request.POST.get('action') == 'Check Out':
            ShoppingCartItem.objects.filter(status="selected").update(status="pending")
            pending_cart_items = ShoppingCartItem.objects.filter(status="pending")
            for pending_cart_item in pending_cart_items:
                if request.POST.get('quantity'+str(pending_cart_item.id)):
                    num = int(request.POST.get('quantity'+str(pending_cart_item.id)))
                    ShoppingCartItem.objects.filter(id=pending_cart_item.id).update(quantity=num)

            selected_items_ids = request.POST.getlist("checkItem")

            for selected_items_id in selected_items_ids:
                ShoppingCartItem.objects.filter(id=selected_items_id).update(status="selected")

        elif request.POST.get('action') == 'Delete Selected':
            return delete_cart(request)

    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})

    if shopping_cart:
        item_cnt = shopping_cart.count_not_deleted_products()

    shipping_fee = get_if_exists(Product, **{'label':"Shipping Fee"})
    if shipping_fee is None:
        shipping_fee = Product.objects.create(label="Shipping Fee", price=200, stock=100000)

    return render(request, "payment/check_out.html", {
        "csss"          : css,
        "jss"           : js,
        "shopping_cart" : shopping_cart,
        "item_cnt"      : item_cnt,
        "shipping_fee"  : shipping_fee
    })


@users_only
def order(request):
    orders = Order.objects.filter(customer=request.user.id)
    order_cnt = len(orders)
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})

    item_cnt = 0
    if shopping_cart:
        item_cnt = shopping_cart.count_not_deleted_products()

    return render(request, "payment/order.html", {
        "csss"      : css,
        "jss"       : js,
        "orders"    : orders,
        "order_cnt" : order_cnt,
        "item_cnt"  : item_cnt
    })


@users_only
def add_order(request, payment):
    customer = request.user
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user})

    new_order = Order.objects.create(customer=customer, payment=payment, status="ongoing")

    shopping_cart_items = shopping_cart.shopping_cart_items()
    for shopping_cart_item in shopping_cart_items:
        if (shopping_cart_item.status == "selected"):
            OrderItem.objects.create(order=new_order, product=shopping_cart_item.product, quantity=shopping_cart_item.quantity, status="ongoing")
            shopping_cart_item.status = "deleted"
            product = shopping_cart_item.product
            product.stock -= shopping_cart_item.quantity
            product.save()
            shopping_cart_item.save()

    shipping_fee = get_if_exists(Product, **{'label':"Shipping Fee"})
    if shipping_fee is None:
        shipping_fee = Product.objects.create(label="Shipping Fee", price=200, stock=100000)

    if(payment.payment_option == "cod"):
        new_order_item = OrderItem(order=new_order, product=shipping_fee, quantity=1, status="Ongoing")
        new_order_item.save()


@users_only
def add_payment(request):
    if request.POST.get('action') == 'ADD PAYMENT':
        customer      = request.user
        address       = request.POST['address']
        mobile_number = request.POST['mobile_number']
        total         = float(request.POST['total'])
        
        if( request.POST['proof_exist'] == "None"):
            proof ="None"
        else:
            proof = request.FILES['proof']

        payment_option = request.POST['payment_option_input']
        new_payment = Payment.objects.create(customer=customer, address=address, mobile_number=mobile_number, total=total, payment_option=payment_option, proof=proof)

        add_order(request, new_payment)

    return redirect("payment:order")


@users_only
def add_cart(request, id):
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})    
    # Check if the product is already in the cart
    if shopping_cart is None:
        shopping_cart = ShoppingCart.objects.create(customer=request.user)

    if request.POST.get('action') == 'ADD TO CART':   
        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        if product.stock == 0:
            messages.add_message(request, messages.ERROR, "This product is out of stock.")
            return redirect("product:product_item", product.id)

        shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart': shopping_cart, 'product': product, 'status': "pending"})
    
        if shopping_cart_item is None:
            shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart': shopping_cart, 'product': product, 'status': "selected"})

        if shopping_cart_item is None:
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
        
        if shopping_cart_item.status == "deleted":
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
        elif shopping_cart_item.status == "ongoing":
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")

        # get the quantity parameter
        quantity = int(request.POST.get('quantity'))
        
        if shopping_cart_item.quantity + quantity >= product.stock:
            shopping_cart_item.quantity = quantity
        else:
            shopping_cart_item.quantity += quantity

        shopping_cart_item.status = "pending"
        shopping_cart_item.save()
        messages.add_message(request, messages.SUCCESS, "Successfully added to shopping cart.")

     
    elif request.POST.get('action') == 'BUY NOW':
        for shopping_cart_item in shopping_cart.shopping_cart_items():
            if shopping_cart_item.status == "selected":
                shopping_cart_item.status = "pending"
                shopping_cart_item.save()

        product = get_if_exists(Product, **{'id':id})
        if product.stock == 0:
            return redirect("product:product_item", product.id)
        shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart':shopping_cart, 'product':product, 'status': "pending"})
    
        if shopping_cart_item is None:
            shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart':shopping_cart, 'product':product, 'status': "selected"})

        if shopping_cart_item is None:
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
        
        if shopping_cart_item.status == "deleted":
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
        elif shopping_cart_item.status == "ongoing":
            shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")

        quantity = int(request.POST.get('quantity'))

        # product.stock -= quantity
        # product.save()
        
        shopping_cart_item.quantity = quantity
        shopping_cart_item.status = "selected"
        shopping_cart_item.save()

        return check_out(request)

    return redirect("product:product_item", product.id)

# @users_only
# def update_item(request, id, quantity):
#     shopping_cart_item = ShoppingCartItem.objects.get(id=id)
#     product            = shopping_cart_item.product
#     quantity           = int(quantity)
           
#     if product.stock > quantity:
#         if quantity < shopping_cart_item.quantity:
#             product.stock += shopping_cart_item.quantity - quantity
#             product.save()
#             shopping_cart_item.quantity = quantity
            

#         elif quantity > shopping_cart_item.quantity:
#             product.stock -=  quantity - shopping_cart_item.quantity 
#             product.save()

#             shopping_cart_item.quantity = quantity
            
#     elif product.stock < quantity:
#         if quantity < shopping_cart_item.quantity:
#             product.stock += shopping_cart_item.quantity - quantity
#             product.save()
#             shopping_cart_item.quantity = quantity
            
#         elif quantity > shopping_cart_item.quantity:
#             if product.stock + shopping_cart_item.quantity < quantity:       
#                 shopping_cart_item.quantity = product.stock + shopping_cart_item.quantity
#                 product.stock = 0
#                 product.save()
                
#             else:
#                 product.stock -= shopping_cart_item.quantity - quantity
#                 product.save()
#                 shopping_cart_item.quantity = quantity
                
#     elif product.stock == 0:
#         pass

#     shopping_cart_item.status = "pending"
#     shopping_cart_item.save()

@users_only
def remove_cart(request, id):
    shopping_cart_item        = ShoppingCartItem.objects.get(id=id)
    shopping_cart_item.status = "deleted"
    shopping_cart_item.save()

    # product           =  shopping_cart_item.product
    # quantity          =  shopping_cart_item.quantity
    # product.stock     += quantity
    # product.save()

    return shopping_cart(request)


@users_only
def check_box(request, id):
    shopping_cart_item = ShoppingCartItem.objects.get(id=id)

    if shopping_cart_item.status == "pending":
        shopping_cart_item.status = "selected"
    elif shopping_cart_item.status == "selected":
        shopping_cart_item.status = "pending"

    shopping_cart_item.save()

    return shopping_cart(request)


@users_only
def delete_cart(request):
    arr = request.POST.getlist("checkItem")
    for i in arr:
        ShoppingCartItem.objects.filter(id=i).update(status="deleted")
    message = request.POST.get('title')

    return shopping_cart(request)