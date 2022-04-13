from cProfile import label
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from sympy import product
from account.forms import AccountAuthenticationForm
from product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# global variables for js and css
js = []
css = []

def login(request):
    page = "login"

    if request.user.is_authenticated: 
        return redirect("management:overview")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                auth_login(request, user)
                return redirect("management:overview")
    else:
        form = AccountAuthenticationForm()

    login_form = form

    return render(request, "management/login.html", {
        "csss" : css,
        "jss"  : js,
        "login_form" : login_form,
        "page" : page
    })

def overview(request):
    page = "overview"

    js = [
        "js/management/raphael-min.js",
        "js/management/morris.min.js",
        "js/management/overview.js",
    ]

    css = [
        "css/management/overview.css",
        "css/management/morris.css"
    ]
    return render(request, "management/overview.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

def inventory(request):
    page = "inventory"

    label = request.GET.get('label')

    sort = request.GET.get('sort')
    # split the sort by '-'
    if sort:
        sort = sort.split('-')
        sort_order = sort[0]
        sort_type = sort[1]

    extra_query = ""

    # get all products from the database
    if label:
        product_list = Product.objects.filter(label__icontains=label)
        extra_query = "&label=" + label
    
    if sort:
        if label:
            product_object = product_list
        else:
            product_object = Product.objects.all()

        if sort_order == "asc":
            product_list = product_object.order_by(sort_type)
            if not label:
                extra_query = "&sort=asc-" + sort_type
        else:
            product_list = product_object.order_by('-' + sort_type)
            if not label:
                extra_query = "&sort=desc-" + sort_type

    if not sort and not label:
        product_list = Product.objects.all()

    # paginate the products
    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        
    return render(request, "management/inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "products" : products,
        "extra_query" : extra_query
    })


def supplies(request):
    page = "supplies"
    return render(request, "management/supplies.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def transactions(request):
    page = "transactions"
    return render(request, "management/transactions.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def account(request):
    page = "account"
    return render(request, "management/account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

def orders(request):
    page = "orders"
    return render(request, "management/orders.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def settings(request):
    page = "settings"
    return render(request, "management/settings.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })
