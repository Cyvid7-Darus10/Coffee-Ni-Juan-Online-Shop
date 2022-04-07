from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField
from django.contrib.postgres.fields import ArrayField
from product.models import Product

class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Order(Base):
    label = models.CharField(max_length=250, blank=True, null=True)
    order_id = models.CharField(max_length=250, blank=True, null=True)
    customer_id = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=30, default="None")
    status = models.CharField(max_length=30, null=True)
    total_payment = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} initiated on {self.created} with status {self.status} and total payment of {self.total_payment}"
    
    class Meta:
        ordering = ['-created']