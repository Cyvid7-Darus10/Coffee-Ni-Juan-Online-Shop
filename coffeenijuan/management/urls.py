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
    path('management/supply', views.supply, name='supply'),
    path('management/add_supply', views.add_supply, name='add_supply'),
    path('management/delete_supply/<int:id>', views.delete_supply, name='delete_supply'),
    path('management/view_supply/<int:id>', views.view_supply, name='view_supply'),
    path('management/edit_supply/<int:id>', views.edit_supply, name='edit_supply'),
    path('management/transactions', views.transactions, name='transactions'),
    path('management/account', views.account, name='account'),
    path('management/add_account', views.add_account, name='add_account'),
    path('management/delete_account/<int:id>', views.delete_account, name='delete_account'),
    path('management/edit_account/<int:id>', views.edit_account, name='edit_account'),
    path('management/view_account/<int:id>', views.view_account, name='view_account'),
    path('management/order_list', views.order_list, name='order_list'),
    path('management/view_order/<int:id>', views.view_order, name='view_order'),
    path('management/cancel_order/<int:id>', views.cancel_order, name='cancel_order'),
    path('management/approve_order/<int:id>', views.approve_order, name='approve_order'),
    path('management/complete_order/<int:id>', views.complete_order, name='complete_order'),
    path('management/settings', views.settings, name='settings'),
]