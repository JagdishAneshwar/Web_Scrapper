from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'),
    path('login.html', views.login, name='login'),
    path('signup.html', views.signup, name='signup'),
    path('home.html', views.home, name='home'),
    path('create_tag', views.create_tag, name='create_tag'),
    path('result', views.result, name='result'),
]
