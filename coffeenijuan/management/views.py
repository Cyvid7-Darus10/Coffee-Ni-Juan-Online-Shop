from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import sort_products, login_user


# global variables for js and css
js = []
css = []

def login(request):
    page = "login"

    if request.user.is_authenticated: 
        return redirect("management:overview")

    login_form = login_user(request)
    if login_form == "redirect":
        return redirect("management:overview")

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

    products, extra_query = sort_products(request)
        
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
