from django.contrib import messages
from .models import *
from django.shortcuts import render, redirect
from .decorators import admin_only

# global variables for js and css
js = []
css = []

@admin_only
def add_inventory(request):
    page = "Inventory | Add Product"
    
    inventory_form = add_inventory_form(request)
    if inventory_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully added product")
        return redirect("management:inventory")

    return render(request, "management/add_inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "inventory_form" : inventory_form
    })

@admin_only
def delete_inventory(request, id):

    result = delete_inventory_item(request, id)

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error deleting product")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully deleted product")

    return redirect("management:inventory")

@admin_only
def view_inventory(request, id):
    page = "Inventory | View Product"

    product_item = get_inventory_item(request, id)

    return render(request, "management/view_inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "product_item" : product_item
    })

@admin_only
def edit_inventory(request, id):
    page = "Inventory | Edit Product"

    inventory_form = edit_inventory_form(request, id)
    if inventory_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully edited product")
        return redirect("management:inventory")

    return render(request, "management/edit_inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "inventory_form" : inventory_form
    })