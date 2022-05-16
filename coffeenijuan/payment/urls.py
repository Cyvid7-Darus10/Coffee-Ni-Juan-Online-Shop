from django.urls import path

from . import views

app_name = "payment"
urlpatterns = [
    # path('check_out', views.check_out, name='check_out'),
    path('check_out/<str:id>/', views.check_out, name='check_out'),
    path('shopping_cart/<str:id>/', views.shopping_cart, name='shopping_cart'),
    path('product_item/<str:id>/', views.product_item, name='product_item'),
]