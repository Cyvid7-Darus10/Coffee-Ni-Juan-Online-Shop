from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from coffeenijuan import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from urllib.parse import quote, unquote
from .support import get_if_exists, encrypt, decrypt
from django.http import HttpResponse
from .models import Account

js = []
css = []

def home(request):
    return render(request, "account/home.html", {
        "csss" : css,
        "jss"  : js
    })

def login_view(request):
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
            subject = "Confirm your Email at Coffee ni Juan Website"
            link = settings.DOMAIN + "/verify/" + quote(encrypt(email + "/" + str(user.id)))
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
<<<<<<< HEAD
    data = decrypted.split('/')
    user = get_if_exists(Account, **{'email':data[0], 'id':data[1]})

    if user:
        user.is_verified = True
        user.save(update_fields=['is_verified'])
    
    return redirect('account:home')
=======
    return HttpResponse("user: {}".format(decrypted))

    pass
>>>>>>> 1d87d5dbc9d4799d287929e577ca38c70ebc3021
