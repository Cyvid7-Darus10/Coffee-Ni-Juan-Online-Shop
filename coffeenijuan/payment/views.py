from django.shortcuts import render,redirect
from .models import Order, OrderItem, ShoppingCart, ShoppingCartItem,Payment
from product.models import Product
from account.support import get_if_exists
from django.shortcuts import redirect
from .decorators import users_only

# global variables for js and css
js = []
css = []


@users_only
def shopping_cart(request):
    cart = get_if_exists(ShoppingCart, customer = request.user.id)
    if cart is None:
        cart = ShoppingCart.objects.create(customer=request.user)
    # get user's shopping cart
    item_cnt = 0
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.countNotDeletedProducts()
    return render(request, "payment/shopping_cart.html", {
        "csss" : css,
        "jss"  : js,
        "cart": cart,
        "item_cnt" : item_cnt
    })


@users_only
def check_out(request):
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
        elif request.POST.get('action') == 'Cancel':
             return delete_cart(request)

    if shopping_cart:
        item_cnt = shopping_cart.countNotDeletedProducts()
            
    return render(request, "payment/check_out.html", {
        "csss" : css,
        "jss"  : js,
        "cart" : shopping_cart,
        "item_cnt" : item_cnt
    })


@users_only
def order(request):
    orders = Order.objects.filter(customer=request.user.id)
    order_cnt = len(orders)
    shopping_cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if shopping_cart:
        item_cnt = shopping_cart.countNotDeletedProducts()
    return render(request, "payment/order.html", {
        "csss" : css,
        "jss"  : js,
        "orders" : orders,
        "order_cnt" : order_cnt,
        "item_cnt" : item_cnt
    })


@users_only
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
            ShoppingCartItem.objects.filter(status="Selected").update(status="Deleted")

    shipping_fee = get_if_exists(Product, **{'label':"Shipping Fee"})
    if(payment.payment_option == "cod"):
        new_order_item = OrderItem(order=new_order, product=shipping_fee, quantity=1, status="Deleted")
        new_order_item.save()


@users_only
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
    return order(request)


@users_only
def add_cart(request, id):
    cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})    
    # Check if the product is already in the cart
    if cart is None:
        cart = ShoppingCart.objects.create(customer=request.user)

    if request.POST.get('action') == 'ADD TO CART':   
        # Check if the product is already in the cart
        product = get_if_exists(Product, **{'id':id})
        if product.stock == 0:
            return redirect("product:product_item", product.id)
        item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product, 'status': "Pending"})
    
        if item is None:
            item = get_if_exists(ShoppingCartItem, **{'shopping_cart':cart, 'product':product, 'status': "Selected"})


        if item is None:
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product, status = "Pending")
        
        if item.status == "Deleted":
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product, status = "Pending")
        elif item.status == "Ongoing":
            item = ShoppingCartItem.objects.create(shopping_cart=cart, product=product, status = "Pending")

        # get the quantity parameter
        quantity = int(request.POST.get('quantity'))
        
        product.stock -= quantity
        product.save()

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
        return check_out(request)

    # redirect to product item page
    return redirect("product:product_item", product.id)


@users_only
def update_item(request,id):
    item = ShoppingCartItem.objects.get(id=id)
    product = item.product
    if request.POST.get('action') == 'Update Cart':
        # get the quantity parameter
        number = 'quantity' + " " +  str(id)
        quantity = request.POST.get(number)
        quantity = int(quantity)
        
        
        if product.stock > quantity:
            if quantity < item.quantity:
                product.stock += item.quantity - quantity
                product.save()
                item.quantity = quantity
                

            elif quantity > item.quantity:
                product.stock -=  quantity - item.quantity 
                product.save()

                item.quantity = quantity
               
        elif product.stock < quantity:
            if quantity < item.quantity:
                product.stock += item.quantity - quantity
                product.save()
                item.quantity = quantity
                
            elif quantity > item.quantity:
                if product.stock + item.quantity < quantity:       
                    item.quantity = product.stock + item.quantity
                    product.stock = 0;
                    product.save()
                    
                else:
                    product.stock -= item.quantity - quantity
                    product.save()
                    item.quantity = quantity
                    
        elif product.stock == 0:
            pass

    item.status = "Pending"
    item.save()
    return shopping_cart(request)


@users_only
def remove_cart(request, id):
    item = ShoppingCartItem.objects.get(id=id)
    product = item.product
    quantity = item.quantity
    product.stock += quantity
    product.save()
    item.status = "Deleted"
    item.save()
    return shopping_cart(request)


@users_only
def check_box(request, id):
    item = ShoppingCartItem.objects.get(id=id)
    if(item.status == "Pending"):
        item.status = "Selected"
    elif(item.status == "Selected"):
        item.status = "Pending"
    item.save()
    return shopping_cart(request)


@users_only
def delete_cart(request):
    checkbox = request.POST.get('selectAll')
    cart = get_if_exists(ShoppingCart, **{'customer':request.user.id})
    if cart:
        products = cart.products();
    if checkbox == 'selectAll':
        for product in products:
            item = ShoppingCartItem.objects.get(id=product.id)
            item.status = "Deleted"
            item.save()
    return shopping_cart(request)