from django.contrib import admin
from .models import Product, Review, Comment

# Created the class for defining the admin view for Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('label', 'price', 'stock', 'created', 'updated')
    list_filter = ('created', 'updated')
    list_editable = ('stock', 'price')
    search_fields = ('label', 'created')

    class Meta:
        model = Product

# Registering the models.
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Comment)