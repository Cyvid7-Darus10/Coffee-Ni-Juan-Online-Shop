from django.urls import path

from . import views

app_name = "login_system"
urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]