from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 
                  'profile_pic', 'bio', 'skills', 'languages', 'role']
        
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_pic', 'bio', 'skills', 'languages', 'role']
        
class UserSearchForm(forms.Form):
    role = forms.ChoiceField(choices=[('tutor', 'Tutor'), ('student', 'Student'), ('both', 'Both')], required=False)
    languages = forms.CharField(max_length=500, required=False)
        
    