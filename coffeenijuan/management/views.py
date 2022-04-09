from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from account.forms import RegistrationForm, AccountAuthenticationForm

# global variables for js and css
js = []
css = []

def login(request):
    page = "login"

    if request.user.is_authenticated: 
        return redirect("management:overview")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                auth_login(request, user)
                return redirect("management:overview")
    else:
        form = AccountAuthenticationForm()

    login_form = form

    return render(request, "management/login.html", {
        "csss" : css,
        "jss"  : js,
        "login_form" : login_form,
        "page" : page
    })

def overview(request):
    page = "overview"
    return render(request, "management/overview.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

def inventory(request):
    page = "inventory"
    return render(request, "management/inventory.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def supplies(request):
    page = "supplies"
    return render(request, "management/supplies.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def transactions(request):
    page = "transactions"
    return render(request, "management/transactions.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def account(request):
    page = "account"
    return render(request, "management/account.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

def orders(request):
    page = "orders"
    return render(request, "management/orders.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })


def settings(request):
    page = "settings"
    return render(request, "management/settings.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })
