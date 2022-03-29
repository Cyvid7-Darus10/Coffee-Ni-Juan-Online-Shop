from django.db import models
from datetime import datetime
from django.db.models.fields import DateTimeField

class Base(models.Model):
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Product(Base):
    label   = models.CharField(max_length=250)
    date    = models.DateField()
    rating  = models.FloatField()
    price   = models.FloatField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.label} on {self.date} with {self.points} points"