from django.urls import path

from . import views

app_name = "management"
urlpatterns = [
    path('management/', views.login, name='login'),
    path('management/login', views.login, name='login'),
    path('management/overview', views.overview, name='overview'),
    path('management/inventory', views.inventory, name='inventory'),
    path('management/add_inventory', views.add_inventory, name='add_inventory'),
    path('management/delete_inventory/<int:id>', views.delete_inventory, name='delete_inventory'),
    path('management/view_inventory/<int:id>', views.view_inventory, name='view_inventory'),
    path('management/edit_inventory/<int:id>', views.edit_inventory, name='edit_inventory'),
    path('management/supplies', views.supplies, name='supplies'),
    path('management/transactions', views.transactions, name='transactions'),
    path('management/account', views.account, name='account'),
    path('management/orders', views.orders, name='orders'),
    path('management/settings', views.settings, name='settings'),
]