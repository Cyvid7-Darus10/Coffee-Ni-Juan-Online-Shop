from django.contrib import admin
from .models import Order, ShoppingCart, OrderItem, ShoppingCartItem, Payment

# Registering the models.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Payment)