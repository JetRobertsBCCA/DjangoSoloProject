from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form=CustomUserCreationForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
class CustomLogoutView(LogoutView):
    template_name = 'users/logged_out.html'
    
@login_required
def profile(request):
    return render(request, 'users/profile.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = '/profile/'
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = '/login/'
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
   template_name = 'users/password_reset_confirm.html'
   success_url = '/login/'
        

