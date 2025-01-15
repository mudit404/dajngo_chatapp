from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Signup URL
    path('signup/', views.signup, name='signup'),
    # Login and logout URLs using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
]