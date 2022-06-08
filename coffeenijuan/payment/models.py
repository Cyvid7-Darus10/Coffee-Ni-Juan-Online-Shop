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

class Payment(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)
    mobile_number = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=30, default="None")
    payment_option = models.CharField(max_length=30, default="None")
    total = models.FloatField(default=0)
    proof = models.ImageField(upload_to ='payment/proof/')

    def __str__(self):
        return f"{self.label} initiated on {self.created}"
    
    class Meta:
        ordering = ['-created']

class Order(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=30, null=True)

    @property
    def products(self):
        return OrderItem.objects.filter(order=self.id)

    def totalPrice(self):
        products = OrderItem.objects.filter(order=self.id)
        price = 0
        for product in products:
            price += product.totalPrice
        return price;

    def __str__(self):
        return f"{self.label} initiated on {self.created} with status {self.status}"
    
    class Meta:
        ordering = ['-created']

class ShoppingCart(Base):   
    label = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)

    @property
    def totalPrice(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        price = 0
        for product in products:
            price += product.totalPrice
        return '{:,}'.format(price)
    
    def totalPricePending(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        price = 0
        for product in products:
            if(product.status == "Pending"):
                price += product.totalPrice
        return '{:,}'.format(price)

    def totalPriceSelected(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        price = 0
        for product in products:
            if(product.status == "Selected"):
                price += product.totalPrice
        return '{:,}'.format(price)

    def totalPriceSelectedInteger(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        price = 0
        for product in products:
            if(product.status == "Selected"):
                price += product.totalPrice
        return price

    def products(self):
        return ShoppingCartItem.objects.filter(shopping_cart=self.id)

    def countNotDeletedProducts(self):
        count = 0
        list_of_products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        for product in list_of_products:
            if(not (product.status == "Deleted" or product.status == "Ongoing")):
                count+=1
        return count

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']

class ShoppingCartItem(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
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

class OrderItem(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
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