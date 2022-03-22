from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path('productList', views.productList, name='productList'),
]