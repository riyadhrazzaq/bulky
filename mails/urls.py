from django.urls import include, path
from django.conf import settings 
from mails import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.home, name='home'),
        path('compose/', views.new, name='new'),
        path('message/<int:pk>/', views.message_detail, name='message'),
        path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
        path('signup/', views.signup_view, name='signup'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('profile/', views.profile_view, name='profile'),
        ] 
