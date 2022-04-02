from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path('product_list', views.product_list, name='product_list'),
    path('product_item/<str:id>/', views.product_item, name='product_item'),
]