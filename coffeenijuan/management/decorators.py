from django.contrib import messages
from django.shortcuts import redirect


# user must be logged in to access this page and is_admin must be true
# declaring the decorator
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page")
            return redirect("account:index")
    return wrapper_function
