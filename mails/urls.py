from django.urls import include, path
from django.conf import settings 
from mails import views

urlpatterns = [
        path('h/', views.home, name='home'),
        path('new/', views.new, name='new'),
        ] 