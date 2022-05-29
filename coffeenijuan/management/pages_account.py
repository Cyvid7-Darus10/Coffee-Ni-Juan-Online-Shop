from django.contrib import messages
from .model_account import *
from django.shortcuts import render, redirect
from .decorators import admin_only

# global variables for js and css
js = []
css = []

@admin_only
def add_account(request):
    page = "Inventory | Add Account"
    
    account_form = add_account_form(request)
    if account_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully added account")
        return redirect("management:account")

    return render(request, "management/account/add_account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "account_form" : account_form
    })

@admin_only
def delete_supply(request, id):

    result = delete_supply_item(request, id)

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error deleting supply")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully deleted supply")

    return redirect("management:supply")

@admin_only
def view_supply(request, id):
    page = "Inventory | View Supply"

    supply_item = get_supply_item(request, id)

    return render(request, "management/supply/view_supply.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "supply_item" : supply_item
    })

@admin_only
def edit_supply(request, id):
    page = "Inventory | Edit Supply"

    supply_form = edit_supply_form(request, id)
    if supply_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully edited supply")
        return redirect("management:supply")

    return render(request, "management/supply/edit_supply.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "supply_form" : supply_form
    })