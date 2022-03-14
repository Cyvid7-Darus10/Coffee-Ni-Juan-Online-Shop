from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from coffeenijuan import settings
from django.core.mail import send_mail
from urllib.parse import quote, unquote
from .support import get_if_exists, encrypt, decrypt
from django.http import HttpResponse, HttpResponseRedirect
from .models import Account
from django.urls import reverse

js = []
css = []

def prompt_message(request, type):
    return HttpResponse(type)
    pass


def home(request):
    css = [
        "/static/css/login/animation.css"
    ]

    js = [
        "/static/js/animations.js"
    ]
    
    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js
    })


def login_view(request):
    css = [
        "/static/css/login/animation.css"
    ]
    js = [
        "/static/js/animations.js"
    ]

    if request.user.is_authenticated: 
        return redirect("account:home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("account:home")
    else:
        form = AccountAuthenticationForm()

    login_form = form

    return render(request, "account/login.html", {
        "csss" : css,
        "jss"  : js,
        "login_form" : login_form
    })


def register(request):
    css = [
        "/static/css/login/animation.css"
    ]

    js = [
        "/static/js/animations.js"
    ]

    if request.user.is_authenticated: 
        return redirect("account:home")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            
            # For email verification

            # --------Email Message--------------
            # User Data
            user = get_if_exists(Account, **{'email':email})

            
            # Sending Welcome Email
            subject = "Welcome to Coffee ni Juan Coffee Shop!!"
            message = "Hello {} {}".format(user.first_name, user.last_name)    
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

            # Sending Verification Email
            link = settings.DOMAIN + "/verify/" + quote(encrypt(email + str(user.id)))
            message = "Hello {} {}, Go to this link to confirm your account: {}".format(user.first_name, user.last_name, link)    
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

    
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
    if request.user.is_authenticated: 
        logout(request)
        
    return redirect('account:home')


def verify(request, token):
    decrypted = decrypt(unquote(token))
    data = decrypted.split('.com')
    
    user = None
    if (data[1].isnumeric()):
        user = get_if_exists(Account, **{'email':data[0] + ".com", 'id':data[1]})

    if user:
        user.is_verified = True
        user.save(update_fields=['is_verified'])
    else:
        url = reverse('account:prompt_message', kwargs={'type':"invalid_token"})
        return HttpResponseRedirect(url)
        
    return redirect('account:home')