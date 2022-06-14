from django.contrib import messages
from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.account_type == "admin"):
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'You are not authorized to access the previous page') 
            return redirect("account:index")
    return wrapper_function


def include_farmer_staff(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.is_authenticated and 
            (request.user.account_type == "farmer"
            or request.user.account_type == "staff"
            or request.user.account_type == "admin")
            ):
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You do not have permission to access the previous page")
            return redirect("account:index")
    return wrapper_function


def include_staff(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.is_authenticated and 
            (request.user.account_type == "staff"
            or request.user.account_type == "admin")
            ):
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You do not have permission to access the previous page")
            return redirect("account:index")
    return wrapper_function
