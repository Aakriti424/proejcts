from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'password', 'email','role', 'address', 'contact']
        read_only_fields=['created_at']


class Login(forms.ModelForm):
    class Meta:
        model=User
        fields=['email', 'password']


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model=JobSeeker
        fields=[ 'resume', 'bio']
        exclude=['job','action']

        


class EmployerForm(forms.ModelForm):
    class Meta:
        model=Employer
        fields=['user','company', 'company_logo', 'post', 'requirement', 'remains_till','website']
        exclude=['user']
        read_only_field=['issued_at']