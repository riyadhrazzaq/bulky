from django.urls import include, path
from django.conf import settings 
from mails import views
urlpatterns = [
        path('h/', views.home, name='home'),
        path('new/', views.new, name='new'),
        path('accounts/', include('django.contrib.auth.urls')),
        path('accounts/signup/', views.signup_view, name='signup'),
        path('accounts/<str:username>/', views.profile_view, name='profile'),
        ] 
