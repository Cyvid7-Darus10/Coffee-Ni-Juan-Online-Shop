from django.contrib import messages
from .models import *
from .helpers import *
from django.shortcuts import render, redirect

# global variables for js and css
js = []
css = []

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

def delete_inventory(request, id):

    result = delete_inventory_item(request, id)

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error deleting product")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully deleted product")

    return redirect("management:inventory")

def view_inventory(request, id):
    page = "Inventory | View Product"

    product_item = get_inventory_item(request, id)

    return render(request, "management/view_inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "product_item" : product_item
    })

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