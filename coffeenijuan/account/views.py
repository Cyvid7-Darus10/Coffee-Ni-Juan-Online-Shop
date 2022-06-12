from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, ForgotPassword
from coffeenijuan import settings
from django.core.mail import send_mail, BadHeaderError
from urllib.parse import quote, unquote
from .support import get_if_exists, encrypt, decrypt
from django.http import HttpResponse, HttpResponseRedirect
from .models import Account
from django.urls import reverse
import datetime
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from product.models import Product
from payment.models import Order, OrderItem, ShoppingCart, ShoppingCartItem, Payment
from product.views import product_item
from django.contrib import messages

js = []
css = []
page = "home"

def prompt_message(request, type):
    page = "prompt_message"

    return render(request, "prompt.html", {
        "type" : type,
        "csss" : css,
        "jss"  : js,
        'page' : page
    })

def home(request):
    page = "home"

     # get all products
    items = Product.objects.all()

    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page,
        "items" :   items
    })

def about(request):
    page = "about"

    return render(request, "about.html", {
        "csss" : css,
        "jss"  : js,
        "page" : page
    })

def login_view(request):
    page = "login"

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
        "login_form" : login_form,
        "page" : page
    })

def register(request):
    page = "register"

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
            link = settings.DOMAIN + "/verify/" + quote(encrypt(email + "+" + str(user.id)))
            message = "Hello {} {}, Go to this link to confirm your account: {}".format(user.first_name, user.last_name, link)    
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

    
            return redirect('account:home')
        else:
            registration_form = form
    else:
        form = RegistrationForm()
        registration_form = form

    js = ['js/registration_form.js']

    return render(request, "account/register.html", {
        "csss" : css,
        "jss"  : js,
        "registration_form" : registration_form,
        "page" : page
    })


def logout_view(request):
    if request.user.is_authenticated: 
        logout(request)
        
    return redirect('account:home')


def verify(request, token):
    decrypted = decrypt(unquote(token))
    data = decrypted.split('+')
    
    user = None
    if (data[1].isnumeric()):
        user = get_if_exists(Account, **{'email':data[0], 'id':data[1]})

    if user:
        user.is_verified = True
        user.save(update_fields=['is_verified'])
    else:
        url = reverse('account:prompt_message', kwargs={'type':"invalid_token"})
        return HttpResponseRedirect(url)
        
    return redirect('account:home')


def forgot_password(request):
    page = "forgot_password"
    
    if request.POST:
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = request.POST['email']

            user = get_if_exists(Account, **{'email':email})

            if user:
                subject = "PASSWORD RECOVERY"
                email_template_name = "password/password_reset_email.txt"
                c = {
					"email": user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}

                email = render_to_string(email_template_name, c)
                from_email = settings.EMAIL_HOST_USER

                try:
                    send_mail(subject, email, from_email , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            url = reverse('account:prompt_message', kwargs={'type':"email_password_reset"})
            return HttpResponseRedirect(url)

    else:
        form = ForgotPassword()

    forgot_form = form

    return render(request, "account/forgot.html", {
        "csss" : css,
        "jss"  : js,
        "forgot_form" : forgot_form,
        "page" : page
    })