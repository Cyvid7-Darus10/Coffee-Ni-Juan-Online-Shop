from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField
from django.contrib.postgres.fields import ArrayField
from product.models import Product
from account.models import Account
from django.db.models import Sum

class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Order(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, default="None")
    status = models.CharField(max_length=30, null=True)
    total_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} initiated on {self.created} with status {self.status} and total price of {self.total_price}"
    
    class Meta:
        ordering = ['-created']

class ShoppingCart(Base):   
    label = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)

    @property
    def totalPrice(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        price = 0
        for product in products:
            price += product.totalPrice
        return price

    def products(self):
        return ShoppingCartItem.objects.filter(shopping_cart=self.id)

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']

class ShoppingCartItem(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30, null=True)

    @property
    def totalPrice(self):
        price = self.product.price
        quantity = self.quantity
        total = price*quantity
        return total

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']