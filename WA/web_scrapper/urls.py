from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login.html', views.login, name='login'),
    path('signup.html', views.signup, name='signup'),
    path('home.html', views.home, name='home'),
    path('tags.html', views.tag, name='tag'),
    path('tags.html/<int:pk>/', views.tag, name='tag'),
    path('result.html', views.result, name='result'),
    path('delete_tag/<item_id>', views.delete_tag, name='delete_tag'),
    path('submit/', views.result, name='filter'),
]
