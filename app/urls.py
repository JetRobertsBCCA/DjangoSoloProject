from django.urls import path, include
from . import views
from django.contrib import admin
from .views import register, CustomLoginView, CustomLogoutView, profile, CustomPasswordChangeView, CustomPasswordResetView, CustomPasswordResetConfirmView, search_users

urlpatterns = [
     path('register/', register, name='register'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/', CustomLogoutView.as_view(), name='logout'),
     path('profile/', views.my_profile, name='profile'),
     path('edit-profile/', views.edit_profile, name='edit_profile'),
     path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
     path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('search/', search_users, name='search_users'),
     path('profile/<str:username>/', views.profile, name='user_profile'),
     path('send_request/', views.send_request, name='send_request'),
     path('manage_requests/', views.manage_requests, name='manage_requests'),
     path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
     path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
     path('delete-profile/', views.delete_profile, name='delete_profile'),

]
