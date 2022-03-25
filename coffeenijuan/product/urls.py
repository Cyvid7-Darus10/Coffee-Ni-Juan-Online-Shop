from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path('product', views.index, name='index'),
]