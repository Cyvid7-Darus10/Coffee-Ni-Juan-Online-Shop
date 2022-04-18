from django.contrib import admin
from .models import Order, ShoppingCart, ShoppingCartItem

# Registering the models.
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)