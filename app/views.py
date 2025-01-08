from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserEditForm, UserSearchForm, TutorCreationForm, StudentCreationForm, StudentTutorRequestForm
from .models import CustomUser, Tutor, Student, StudentTutorRequest
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def delete_profile(request):
    if request.method == 'POST':
        confirmation_text = f"My name is {request.user.username}, and I am going to delete my account"
        user_input = request.POST.get('confirmation', '')

        if user_input == confirmation_text:
            user = request.user
            logout(request)  
            user.delete()  
            return redirect('home')  

    return render(request, 'users/delete_profile.html', {'username': request.user.username})


@login_required
def search_users(request):
    form = UserSearchForm()
    users = CustomUser.objects.none()
    if request.method == 'GET' and (request.GET.get('role') or request.GET.get('languages')):
        role = request.GET.get('role')
        languages = request.GET.get('languages')

        users = CustomUser.objects.all() 
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
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        if 'tutor' in request.POST:
            tutor_form = TutorCreationForm(request.POST)
            if user_form.is_valid() and tutor_form.is_valid():
                user = user_form.save(commit=False)
                user.role = 'tutor'  # Automatically assign the tutor role
                user.save()
                tutor = tutor_form.save(commit=False)
                tutor.user = user
                tutor.save()
                return redirect('home')
        elif 'student' in request.POST:
            student_form = StudentCreationForm(request.POST)
            if user_form.is_valid() and student_form.is_valid():
                user = user_form.save(commit=False)
                user.role = 'student'  # Automatically assign the student role
                user.save()
                student = student_form.save(commit=False)
                student.user = user
                student.save()
                return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        tutor_form = TutorCreationForm()
        student_form = StudentCreationForm()
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'tutor_form': tutor_form,
        'student_form': student_form
    })

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    

@login_required
def my_profile(request):
    user = request.user
    if hasattr(user, 'tutor'):
        students = user.tutor.students.all()
    else:
        students = None

    return render(request, 'users/profile.html', {
        'user': user,
        'students': students
    })

@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    show_request_button = False
    request_sent = False

    if hasattr(user, 'tutor') and hasattr(request.user, 'student'):
        # Check if the logged-in user is a student and doesn't already have a tutor
        if request.user.student.tutor is None:
            show_request_button = True
            # Check if a request has already been sent
            request_sent = StudentTutorRequest.objects.filter(student=request.user.student, tutor=user.tutor).exists()

    if hasattr(user, 'tutor'):
        students = user.tutor.students.all()
    else:
        students = None

    return render(request, 'users/profile.html', {
        'user': user,
        'students': students,
        'show_request_button': show_request_button,
        'request_sent': request_sent
    })

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
        
@login_required
def send_request(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_id')
        tutor = get_object_or_404(Tutor, id=tutor_id)
        student = get_object_or_404(Student, user=request.user)

        # Check if the student already has a tutor
        if student.tutor is None:
            StudentTutorRequest.objects.create(student=student, tutor=tutor)
            return redirect('user_profile', username=tutor.user.username)

    return redirect('home')

@login_required
def manage_requests(request):
    tutor = get_object_or_404(Tutor, user=request.user)
    pending_requests = StudentTutorRequest.objects.filter(tutor=tutor, status='pending')
    has_pending_requests = pending_requests.exists()
    return render(request, 'users/manage_requests.html', {'requests': pending_requests, 'has_pending_requests': has_pending_requests})

@login_required
def accept_request(request, request_id):
    request_instance = get_object_or_404(StudentTutorRequest, id=request_id, tutor__user=request.user)
    request_instance.status = 'accepted'
    request_instance.save()

    tutor = request_instance.tutor
    student = request_instance.student
    tutor.students.add(student)

    
    student.tutor = tutor
    student.save()

    return redirect('manage_requests')

@login_required
def reject_request(request, request_id):
    request_instance = get_object_or_404(StudentTutorRequest, id=request_id, tutor__user=request.user)
    request_instance.status = 'rejected'
    request_instance.save()
    return redirect('manage_requests')