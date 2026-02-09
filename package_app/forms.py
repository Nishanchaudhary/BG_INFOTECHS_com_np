from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'icon', 'title', 'image', 'month_price', 'year_price', 
            'short_desc', 'description', 'graphic_design', 'motion_graphic',
            'shute_video', 'content_video', 'real', 'bosting', 'status', 'tags'
        ]
        widgets = {
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-star, bi bi-gem'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter package title'
            }),
            'month_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly price'
            }),
            'year_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Yearly price'
            }),
            'short_desc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Short description (max 300 characters)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description'
            }),
            'graphic_design': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Graphic design details'
            }),
            'motion_graphic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motion graphic details'
            }),
            'shute_video': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shute video details'
            }),
            'content_video': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Content video details'
            }),
            'real': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reel details'
            }),
            'bosting': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bosting details'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comma separated tags'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})