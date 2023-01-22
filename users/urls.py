from django.urls import path, include
from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('users', include('django.contrib.auth.urls'), name='users'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signup/register', views.register, name='register'),
    path('logout', views.logout, name='logout')
]
