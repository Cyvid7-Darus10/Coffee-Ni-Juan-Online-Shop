from django.contrib.auth import login as auth_login, authenticate
from account.forms import AccountAuthenticationForm
from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField


def login_user(request):
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                auth_login(request, user)
                return "redirect"
    else:
        form = AccountAuthenticationForm()
    
    return form

class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Supply(Base):
    label       = models.CharField(max_length=250, blank=True, null=True)
    price       = models.FloatField(blank=True, null=True)
    stock       = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} on {self.created} with {self.price} price"
    
    class Meta:
        ordering = ['-created']