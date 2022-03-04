from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm

js = []
css = []

def home(request):
    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js
    })

def login_view(request):
    return render(request, "account/login.html", {
        "csss" : css,
        "jss"  : js
    })

def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('account:home')
        else:
            registration_form = form
    else:
        form = RegistrationForm()
        registration_form = form

    return render(request, "account/register.html", {
        "csss" : css,
        "jss"  : js,
        "registration_form" : registration_form
    })

def logout_view(request):
	logout(request)
	return redirect('account:home')