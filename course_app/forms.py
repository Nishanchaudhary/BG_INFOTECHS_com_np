from django import forms
from .models import Course, Media, CourseEnrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'image', 'short_description', 'description', 
            'duration', 'price', 'offer_price', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter short description (max 500 characters)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter detailed course description'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DD HH:MM:SS or HH:MM:SS (e.g., 5 00:00:00 for 5 days)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Enter regular price'
            }),
            'offer_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Enter offer price (optional)'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(True, 'Active'), (False, 'Inactive')]),
        }
    
    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration and duration.total_seconds() <= 0:
            raise forms.ValidationError("Duration must be greater than zero.")
        return duration
    
    def clean_offer_price(self):
        offer_price = self.cleaned_data.get('offer_price')
        price = self.cleaned_data.get('price')
        
        if offer_price and price and offer_price >= price:
            raise forms.ValidationError("Offer price must be less than regular price.")
        
        return offer_price

# forms.py
class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        # METHOD 1: Exclude course field (RECOMMENDED)
        exclude = ['course']
        
        # OR METHOD 2: Explicitly list fields without course
        # fields = ['media_type', 'file', 'caption', 'order', 'status']
        
        widgets = {
            'media_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter media caption'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Auto-assign if empty'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make file field optional for updates, required for creates
        if self.instance and self.instance.pk:
            self.fields['file'].required = False
            self.fields['file'].help_text = "Leave empty to keep existing file"
        else:
            self.fields['file'].required = True
            self.fields['file'].help_text = "Required for new media"

class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = [
            'first_name', 'last_name', 'email', 'contact_number', 'address',
            'education', 'experience', 'source'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3
            }),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

MediaInlineFormSet = forms.inlineformset_factory(
    Course, 
    Media, 
    form=MediaForm, 
    extra=1,
    can_delete=True
)