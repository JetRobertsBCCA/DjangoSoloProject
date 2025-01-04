from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Tutor, Student, StudentTutorRequest

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 
                  'profile_pic', 'bio', 'skills', 'languages', 'contact_email']
        
class TutorCreationForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['hourly_rate']
        
class StudentTutorRequestForm(forms.ModelForm):
    class Meta:
        model = StudentTutorRequest
        fields = ['tutor']

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['max_budget']

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_pic', 'bio', 'skills', 'languages', 'role', 'contact_email']

        
class UserSearchForm(forms.Form):
    role = forms.ChoiceField(choices=[('tutor', 'Tutor'), ('student', 'Student')], required=False)
    languages = forms.CharField(max_length=500, required=False)

        
    