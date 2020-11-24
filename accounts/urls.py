from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('regular', views.regular, name='regular'),
    path('company', views.company, name='company'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout')
]
