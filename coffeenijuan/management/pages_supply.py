from django.contrib import messages
from .model_supply import *
from django.shortcuts import render, redirect
from .decorators import include_farmer_staff

# global variables for js and css
js = []
css = []

@include_farmer_staff
def add_supply(request):
    page = "Inventory | Add Supply"
    
    supply_form = add_supply_form(request)
    if supply_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully added supply")
        return redirect("management:supply")

    return render(request, "management/supply/add_supply.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "supply_form" : supply_form
    })

@include_farmer_staff
def delete_supply(request, id):

    result = delete_supply_item(request, id)

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error deleting supply")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully deleted supply")

    return redirect("management:supply")

@include_farmer_staff
def view_supply(request, id):
    page = "Inventory | View Supply"

    supply_item = get_supply_item(request, id)

    return render(request, "management/supply/view_supply.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "supply_item" : supply_item
    })

@include_farmer_staff
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