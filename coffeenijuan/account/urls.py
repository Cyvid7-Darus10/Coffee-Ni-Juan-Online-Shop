from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('verify/<str:token>/', views.verify, name='verify'),
    path('prompt_message/<str:type>/', views.prompt_message, name='prompt_message'),
]