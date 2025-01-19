from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
  class Meta:
    model = ServiceRequest
    fields = ['service_type', 'description', 'attachments']
    widgets = {
        'description': forms.Textarea(attrs={'rows': 4}),
    }
    labels = {
        'service_type': 'Type of Service Request',
        'description': 'Please provide a detailed description of your request',
    }
    help_texts = {
        'description': 'The more details you provide, the better we can assist you.',
    }
    def clean_description(self):
        # Optional: Perform additional validation on the description field
        cleaned_data = self.cleaned_data['description']
        if len(cleaned_data) < 50:
            raise forms.ValidationError('Description must be at least 50 characters long.')
        return cleaned_data