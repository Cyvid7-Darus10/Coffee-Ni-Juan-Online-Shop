from django.shortcuts import render, redirect
from .models import *
from .extra_inventory import *
from .helpers import excelreport
from .decorators import admin_only

# global variables for js and css
js = []
css = []

def login(request):
    page = "login"

    if request.user.is_authenticated and request.user.is_admin: 
        return redirect("management:overview")

    login_form = login_user(request)

    return render(request, "management/login.html", {
        "csss" : css,
        "jss"  : js,
        "login_form" : login_form,
        "page" : page
    })

@admin_only
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

@admin_only
def inventory(request):
    page = "inventory"

    # Check if the user wants to export the inventory
    if request.GET.get("export"):
        products = get_inventory_items(request)
        return excelreport(request, products, "inventory")

    products, extra_query = sort_products(request)
        
    return render(request, "management/inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "products" : products,
        "extra_query" : extra_query
    })

@admin_only
def supplies(request):
    page = "supplies"
    return render(request, "management/supplies.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

@admin_only
def transactions(request):
    page = "transactions"
    return render(request, "management/transactions.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

@admin_only
def account(request):
    page = "account"
    return render(request, "management/account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

@admin_only
def orders(request):
    page = "orders"
    return render(request, "management/orders.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

@admin_only
def settings(request):
    page = "settings"
    return render(request, "management/settings.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })
