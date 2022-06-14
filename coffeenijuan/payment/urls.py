from django.urls import path

from . import views

app_name = "payment"
urlpatterns = [
    path('check_out/', views.check_out, name='check_out'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('order/', views.order, name='order'),
    path('check_box/<str:cart>/', views.check_box, name='check_box'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('add_cart/<str:id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    # path('update_item/<str:id>/<int:quantity>/', views.update_item, name='update_item'),
    path('shopping_cart/<str:id>/', views.shopping_cart, name='shopping_cart'),
]