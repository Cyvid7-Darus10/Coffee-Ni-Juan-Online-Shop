from django.contrib import messages
from django.shortcuts import render, redirect
from .decorators import include_staff
from .model_order import *

# global variables for js and css
js = []
css = []

@include_staff
def complete_order(request, id):

    result = update_order_status(request, id, "completed")

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error completing order")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully completed order")

    return redirect("management:order_list")


@include_staff
def approve_order(request, id):

    result = update_order_status(request, id, "approved")

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error approving order")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully approved order")

    return redirect("management:order_list")


@include_staff
def cancel_order(request, id):

    result = update_order_status(request, id, "cancelled")

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error cancelling order")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully cancelled order")

    return redirect("management:order_list")


@include_staff
def view_order(request, id):
    page = "Inventory | View order"

    order = get_order_by_id(request, id)

    return render(request, "management/order/view_order.html", {
        "csss"  : css,
        "jss"   : js,
        "page"  : page,
        "order" : order
    })