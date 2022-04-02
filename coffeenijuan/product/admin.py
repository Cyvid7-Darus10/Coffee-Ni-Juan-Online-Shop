from django.contrib import admin
from .models import Product, Review, Comment

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Comment)