from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('verify/<str:token>/', views.verify, name='verify'),
]