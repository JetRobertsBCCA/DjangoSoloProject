from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView, profile, CustomPasswordChangeView, CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
     path('register/', register, name='register'),
     path('login/', CustomLoginView.as_view(), name='login'),
     path('logout/', CustomLogoutView.as_view(), name='logout'),
     path('profile/', profile, name='profile'),
     path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
     path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     
]
