from django.urls import path, include
from . import views
from django.contrib import admin
from .views import register, CustomLoginView, CustomLogoutView, profile, CustomPasswordChangeView, CustomPasswordResetView, CustomPasswordResetConfirmView, search_users

urlpatterns = [
     path('register/', register, name='register'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/', CustomLogoutView.as_view(), name='logout'),
     path('profile/', views.profile, name='profile'),
     path('edit-profile/', views.edit_profile, name='edit_profile'),
     path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
     path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('search/', search_users, name='search_users'),
     
]
