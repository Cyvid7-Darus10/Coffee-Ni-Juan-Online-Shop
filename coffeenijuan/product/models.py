from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField
from account.models import Account

class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Product(Base):
    label       = models.CharField(max_length=250, blank=True, null=True)
    image_url   = models.CharField(max_length=150, null=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock       = models.PositiveIntegerField(default=0)
    rating      = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} on {self.date} with {self.price} price"

    class Meta:
        ordering = ['-created']


class Review(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author  = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating  = models.FloatField(blank=True, null=True)
    text    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.author} on {self.product.label} with {self.rating} points"

    def __repr__(self):
        return f"<Review {self.author} on {self.product.label} with {self.rating} points>"

    @property
    def points(self):
        return self.rating

    class Meta:
        ordering = ['-rating']


class Comment(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author  = models.ForeignKey(Account, on_delete=models.CASCADE)
    text    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.author} on {self.product.label}"

    def __repr__(self):
        return f"<Comment {self.author} on {self.product.label}"

    class Meta:
        ordering = ['-created']