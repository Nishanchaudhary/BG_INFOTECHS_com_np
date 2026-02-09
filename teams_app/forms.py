from django import forms
from .models import Teams

class TeamsForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields = [
            'name', 'image', 'phone', 'email', 'facebook', 'twitter', 
            'linkedin', 'tiktok', 'designation', 'description', 
            'skills', 'status', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter designation/role'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter description about the team member'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter skills separated by commas (e.g., Python, Django, JavaScript)'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/username'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://x.com/username'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'tiktok': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://tiktok.com/@username'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Basic phone validation
        if phone and not phone.replace(' ', '').replace('-', '').replace('+', '').isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
    
    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if skills:
            # Validate that skills are comma-separated
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            if len(skills_list) == 0:
                raise forms.ValidationError("Please enter at least one skill.")
        return skills