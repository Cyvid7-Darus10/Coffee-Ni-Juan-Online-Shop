from django.contrib.auth import login as auth_login, authenticate
from account.forms import AccountAuthenticationForm
from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField
from account.models import Account


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
    added_by    = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.label} on {self.created} with {self.price} price"
    
    class Meta:
        ordering = ['-created']


class Transaction(Base):
    action_type = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    action_id   = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.action_type} on {self.created} with {self.description}"

    class Meta:
        ordering = ['-created']


class Analytic(Base):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    action_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    ip_address  = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created']


def add_transaction(action_type, description, user, action_id):
    Transaction.objects.create(action_type=action_type, description=description, user=user, action_id=action_id)

def get_total_vistors():
    return Analytic.objects.all().count()

def get_unique_vistors():
    analytics = Analytic.objects.all()
    # count the number of unique users
    unique_users = set()
    for analytic in analytics:
        unique_users.add(analytic.ip_address)

    return len(unique_users)