from django.contrib import messages
from .model_account import *
from django.shortcuts import render, redirect
from .decorators import admin_only

# global variables for js and css
js = []
css = []

@admin_only
def add_account(request):
    page = "Account | Add Account"
    
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
def delete_account(request, id):

    result = delete_account_item(request, id)

    if result == "error":
        messages.add_message(request, messages.ERROR, "Error deleting account")
    elif result == "success":
        messages.add_message(request, messages.SUCCESS, "Successfully deleted account")

    return redirect("management:account")

@admin_only
def edit_account(request, id):
    page = "Account | Edit account"

    account_form = edit_account_form(request, id)
    if account_form == "redirect":
        messages.add_message(request, messages.SUCCESS, "Successfully edited account")
        return redirect("management:account")

    return render(request, "management/account/edit_account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "account_form" : account_form
    })

@admin_only
def view_account(request, id):
    page = "Account | View Account"

    account = get_account_by_id(request, id)

    return render(request, "management/account/view_account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "account" : account
    })