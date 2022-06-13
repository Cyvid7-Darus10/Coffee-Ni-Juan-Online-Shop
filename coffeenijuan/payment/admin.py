from django.contrib import admin
from .models import Order, ShoppingCart, OrderItem, ShoppingCartItem, Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('label', 'customer', 'total', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('label', 'created')

    class Meta:
        model = Payment

class OrderAdmin(admin.ModelAdmin):
    list_display = ('label', 'customer', 'payment', 'status', 'created', 'updated')
    list_filter = ('created', 'updated')
    list_editable = ('status',)
    search_fields = ('label', 'created')

    class Meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'order', 'product', 'quantity', 'status', 'created', 'updated')
    list_filter = ('created', 'updated')
    list_editable = ('status',)
    search_fields = ('label', 'created')

    class Meta:
        model = OrderItem


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('label', 'customer', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('label', 'created')

    class Meta:
        model = ShoppingCart


class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'shopping_cart', 'product', 'quantity', 'status', 'created', 'updated')
    list_filter = ('created', 'updated')
    list_editable = ('status',)
    search_fields = ('label', 'created')

    class Meta:
        model = ShoppingCartItem


# Registering the models.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)
admin.site.register(Payment, PaymentAdmin)