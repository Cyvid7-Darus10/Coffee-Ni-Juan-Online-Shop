from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField
from django.contrib.postgres.fields import ArrayField
from product.models import Product
from account.models import Account


class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Payment(Base):
    label          = models.CharField(max_length=250, blank=True, null=True)
    customer       = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)
    mobile_number  = models.CharField(max_length=250, blank=True, null=True)
    address        = models.CharField(max_length=30, default="None")
    payment_option = models.CharField(max_length=30, default="None")
    total          = models.FloatField(default=0)
    proof          = models.ImageField(upload_to ='payment/proof/')

    def __str__(self):
        return self.payment_option
    
    class Meta:
        ordering = ['-created']


class Order(Base):
    label    = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)
    payment  = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None, null=True)
    status   = models.CharField(max_length=30, null=True)

    @property
    def order_items(self):
        return OrderItem.objects.filter(order=self.id)

    def total_price(self):
        order_items = OrderItem.objects.filter(order=self.id)
        total = 0
        for order_item in order_items:
            total += order_item.product.price
        return total

    def __str__(self):
        return f"{self.label} initiated on {self.created} with status {self.status}"
    
    class Meta:
        ordering = ['-created']


class OrderItem(Base):
    label    = models.CharField(max_length=250, blank=True, null=True)
    order    = models.ForeignKey(Order, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    status   = models.CharField(max_length=30, null=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']


class ShoppingCart(Base):   
    label    = models.CharField(max_length=250, blank=True, null=True)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True)

    @property
    def total_price(self):
        productsActive = ShoppingCartItem.objects.filter(shopping_cart=self.id, status="selected")
        productsPending = ShoppingCartItem.objects.filter(shopping_cart=self.id, status="Pending")
        price = 0
        for product in productsActive:
            price += product.total_price
        for product in productsPending:
            price += product.total_price
        return '{:,}'.format(price)

    def total_price_selected(self):
        productsSelected = ShoppingCartItem.objects.filter(shopping_cart=self.id, status="selected")
        price = 0
        for product in productsSelected:
            price += product.total_price
        return '{:,}'.format(price)

    def total_price_selected_integer(self):
        products = ShoppingCartItem.objects.filter(shopping_cart=self.id, status="selected")
        price = 0
        for product in products:
            price += product.total_price
        return price

    def shopping_cart_items(self):
        return ShoppingCartItem.objects.filter(shopping_cart=self.id)

    def count_not_deleted_products(self):
        count = 0
        list_of_products = ShoppingCartItem.objects.filter(shopping_cart=self.id)
        for product in list_of_products:
            if(not (product.status == "deleted" or product.status == "ongoing")):
                count+=1
        return count

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']


class ShoppingCartItem(Base):
    label         = models.CharField(max_length=250, blank=True, null=True)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity      = models.PositiveIntegerField(default=0)
    status        = models.CharField(max_length=30, null=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.label} created on {self.created}"
    
    class Meta:
        ordering = ['-created']