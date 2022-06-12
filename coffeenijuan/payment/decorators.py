from django.contrib import messages
from django.shortcuts import redirect


def users_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'You must be logged in to access the previous page') 
            return redirect("account:login")
    return wrapper_function