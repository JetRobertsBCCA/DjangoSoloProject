from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserEditForm, UserSearchForm
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

# Create your views here.

def search_users(request):
    form = UserSearchForm()
    users = CustomUser.objects.all() 
    if request.method == 'GET':
        role = request.GET.get('role')
        languages = request.GET.get('languages')

        if role:
            users = users.filter(role=role)
        if languages:
            users = users.filter(languages__icontains=languages) 

    return render(request, 'users/search.html', {'form': form, 'users': users})


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
    template_name = 'users/logout.html'
    

@login_required
def my_profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile.html', {'user': user})

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
   
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form':form})
        

