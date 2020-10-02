from django.urls import include, path
from django.conf import settings 
from mails import views
urlpatterns = [
        path('h/', views.home, name='home'),
        path('new/', views.new, name='new'),
        path('message/<int:pk>/', views.message_detail, name='message'),
        path('accounts/', include('django.contrib.auth.urls')),
        path('accounts/signup/', views.signup_view, name='signup'),
        path('accounts/profile/', views.profile_view, name='profile'),
        ] 
