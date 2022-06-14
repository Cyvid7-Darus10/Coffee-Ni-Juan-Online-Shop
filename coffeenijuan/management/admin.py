from django.contrib import admin
from .models import Supply, Transaction, Analytic


class SupplyAdmin(admin.ModelAdmin):
    list_display = ('label', 'price', 'stock', 'description', 'added_by', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('label', 'created')

    class Meta:
        model = Supply


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'description', 'user', 'action_id', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('label', 'created')

    class Meta:
        model = Transaction


class AnalyticAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'description', 'ip_address', 'created', 'updated')
    list_filter = ('created', 'updated')

    class Meta:
        model = Analytic


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Analytic, AnalyticAdmin)