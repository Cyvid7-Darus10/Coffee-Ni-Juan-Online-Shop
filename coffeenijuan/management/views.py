from django.shortcuts import render, redirect
from .models import login_user
from .model_transaction import sort_transactions
from .pages_inventory import *
from .pages_supply import *
from .pages_account import *

##Account
from .pages_account import *

from .model_transaction import *
from .helpers import excelreport
from .decorators import admin_only

# global variables for js and css
js = []
css = []

def login(request):
    page = "login"

    login_form = login_user(request)

    if request.user.is_authenticated and request.user.is_admin: 
        return redirect("management:overview")

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
        
    return render(request, "management/inventory/inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "products" : products,
        "extra_query" : extra_query
    })

@admin_only
def supply(request):
    page = "supply"

    # Check if the user wants to export the inventory
    if request.GET.get("export"):
        products = get_supply_items(request)
        return excelreport(request, products, "supply")

    supplies, extra_query = sort_supplies(request)

    return render(request, "management/supply/supply.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "supplies" : supplies,
        "extra_query" : extra_query
    })

@admin_only
def transactions(request):
    page = "transactions"

    transactions, extra_query = sort_transactions(request)

    return render(request, "management/transactions.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "transactions" : transactions,
        "extra_query" : extra_query
    })


@admin_only
def account(request):
    page = "account"

    accounts, extra_query = sort_accounts(request)

    return render(request, "management/account/account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "accounts" : accounts,
        "extra_query" : extra_query
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
