from django import forms
from django.forms import inlineformset_factory
from .models import Training, TrainingImage

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'image', 'duration', 'description', 'price', 'offer_price', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter training title...',
                'id': 'title'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30 days, 2 weeks...',
                'id': 'duration'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control summernote',
                'placeholder': 'Enter detailed description...',
                'rows': 4,
                'id': 'description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter original price...',
                'id': 'price'
            }),
            'offer_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter offer price...',
                'id': 'offer_price'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'status'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'image'
            })
        }
        labels = {
            'title': 'Training Title',
            'image': 'Main Image',
            'duration': 'Duration',
            'description': 'Description',
            'price': 'Original Price (₹)',
            'offer_price': 'Offer Price (₹)',
            'status': 'Active Status'
        }

class TrainingImageForm(forms.ModelForm):
    class Meta:
        model = TrainingImage
        fields = ['image', 'status', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Select additional image...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order...',
                'min': 0
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

TrainingImageFormSet = inlineformset_factory(
    Training,
    TrainingImage,
    form=TrainingImageForm,
    extra=3,
    can_delete=True,
    min_num=0,
    validate_min=True
)