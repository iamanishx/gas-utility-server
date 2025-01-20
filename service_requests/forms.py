from django import forms
from .models import ServiceRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description']


class SupportResponseForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'response']
        
class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description', 'attachments']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    phone_number = forms.CharField(max_length=15, required=True, help_text="Enter your phone number.")
    address = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter your address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')        
