import re
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Order, OrderItem, ShoppingCart, ShoppingCartItem, Payment
from product.models import Product
from account.support import get_if_exists
from django.shortcuts import redirect
from .decorators import users_only
from .forms import AccountUpdateForm
from account.models import Account

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

            if len(selected_items_ids) == 0:
                messages.error(request, "Please select at least one item to check out.")
                return redirect("payment:shopping_cart")

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
        
    account = Account.objects.get(id=request.user.id)
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(instance=account)

    return render(request, "payment/order.html", {
        "csss"      : css,
        "jss"       : js,
        "orders"    : orders,
        "order_cnt" : order_cnt,
        "item_cnt"  : item_cnt,
        "form"      : form
    })


@users_only
def add_order(request, payment):
    customer = request.user
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user})

    new_order = Order.objects.create(customer=customer, payment=payment, status="ongoing")

    shopping_cart_items = shopping_cart.shopping_cart_items()
    for shopping_cart_item in shopping_cart_items:
        if (shopping_cart_item.status == "selected"):
            product = shopping_cart_item.product
            if product.stock < shopping_cart_item.quantity:
                messages.error(request, "Sorry, we don't have enough stock for " + product.label + ".")
                return False
            else:
                OrderItem.objects.create(order=new_order, product=shopping_cart_item.product, quantity=shopping_cart_item.quantity, status="ongoing")
                shopping_cart_item.status = "deleted"
                product.stock -= shopping_cart_item.quantity
                product.save()
                shopping_cart_item.save()

    shipping_fee = get_if_exists(Product, **{'label':"Shipping Fee"})
    if shipping_fee is None:
        shipping_fee = Product.objects.create(label="Shipping Fee", price=200, stock=100000)

    if(payment.payment_option == "cod"):
        new_order_item = OrderItem(order=new_order, product=shipping_fee, quantity=1, status="Ongoing")
        new_order_item.save()

    return True


@users_only
def add_payment(request):
    status = True
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

        status = add_order(request, new_payment)

    if status:
        return redirect("payment:order")
    else:
        return redirect("payment:shopping_cart")
        

def get_shopping_cart(shopping_cart, product):
    shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart': shopping_cart, 'product': product, 'status': "pending"})
    
    if shopping_cart_item is None:
        shopping_cart_item = get_if_exists(ShoppingCartItem, **{'shopping_cart': shopping_cart, 'product': product, 'status': "selected"})

    if shopping_cart_item is None:
        shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
    
    if shopping_cart_item.status == "deleted":
        shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")
    elif shopping_cart_item.status == "ongoing":
        shopping_cart_item = ShoppingCartItem.objects.create(shopping_cart=shopping_cart, product=product, status = "pending")

    return shopping_cart_item

@users_only
def add_cart(request, id):
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})    

    if shopping_cart is None:
        shopping_cart = ShoppingCart.objects.create(customer=request.user)

    quantity = int(request.POST.get('quantity'))

    if request.POST.get('action') == 'ADD TO CART':
        product = get_if_exists(Product, **{'id':id})
        if product.stock == 0:
            messages.add_message(request, messages.ERROR, "This product is out of stock.")
            return redirect("product:product_item", product.id)

        shopping_cart_item = get_shopping_cart(shopping_cart, product)
        
        if shopping_cart_item.quantity + quantity >= product.stock:
            shopping_cart_item.quantity = product.stock
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
            messages.add_message(request, messages.ERROR, "This product is out of stock.")
            return redirect("product:product_item", product.id)
            
        shopping_cart_item = get_shopping_cart(shopping_cart, product)

        shopping_cart_item.quantity = quantity
        shopping_cart_item.status = "selected"
        shopping_cart_item.save()

        return redirect("payment:check_out")

    return redirect("product:product_item", product.id)


@users_only
def remove_cart(request, id):
    shopping_cart_item        = ShoppingCartItem.objects.get(id=id)
    shopping_cart_item.status = "deleted"
    shopping_cart_item.save()
    messages.add_message(request, messages.SUCCESS, "Successfully removed from shopping cart.")
    return redirect("payment:shopping_cart")


@users_only
def check_box(request, id):
    shopping_cart_item = ShoppingCartItem.objects.get(id=id)

    if shopping_cart_item.status == "pending":
        shopping_cart_item.status = "selected"
    elif shopping_cart_item.status == "selected":
        shopping_cart_item.status = "pending"

    shopping_cart_item.save()

    return redirect("payment:shopping_cart")


@users_only
def delete_cart(request):
    arr = request.POST.getlist("checkItem")
    for i in arr:
        ShoppingCartItem.objects.filter(id=i).update(status="deleted")
    
    if len(arr) > 0:
        messages.success(request, "Selected item(s) have been deleted.")
    
    return redirect("payment:shopping_cart")