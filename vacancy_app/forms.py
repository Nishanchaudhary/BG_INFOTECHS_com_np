from django import forms
from .models import Vacancy,JobApplication

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            'title', 'job_type', 'image', 'address', 'short_description',
            'description', 'skills', 'salary', 'expired_date', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location/address'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter short description (max 200 characters)'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter skills separated by commas (e.g., Python, Django, JavaScript)'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary amount'
            }),
            'expired_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'summernote'
    }))
    
  
    
    def clean_expired_date(self):
        expired_date = self.cleaned_data.get('expired_date')
        from django.utils import timezone
        if expired_date and expired_date < timezone.now().date():
            raise forms.ValidationError("Expired date cannot be in the past.")
        return expired_date

class JobApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must consent to data processing.'}
    )
    
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'cover_letter', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us why you\'re a great fit for this position...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            })
        }
        labels = {
            'full_name': 'Full Name*',
            'email': 'Email*',
            'phone': 'Phone*',
            'cover_letter': 'Cover Letter (Optional)',
            'resume': 'Upload Resume PDF*',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        for field in ['full_name', 'email', 'phone', 'resume']:
            self.fields[field].required = True
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Validate file type
            valid_extensions = ['.pdf']
            extension = '.' + resume.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('Please upload a PDF or Word document (PDF, DOC, DOCX).')
            
            # Validate file size (5MB limit)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 5MB.')
        
        return resume
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation - you can enhance this
        if phone and len(phone) < 10:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone
    
    