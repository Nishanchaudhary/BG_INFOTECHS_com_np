from django import forms
from .models import Branch

class BranchForm(forms.ModelForm):
    phone_numbers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone numbers separated by commas',
            'rows': 3
        }),
        help_text="Enter multiple phone numbers separated by commas"
    )
    
    class Meta:
        model = Branch
        fields = [
            'name', 'maps', 'image', 'description', 'address', 'email', 
            'office_open', 'status', 'facebook', 'twitter', 'linkedin', 'instagram'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter branch name'
            }),
            'maps': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Google Maps URL'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter branch description',
                'rows': 4
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full address',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'office_open': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mon-Fri 9:00 AM - 6:00 PM'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Facebook URL'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Twitter/X URL'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter LinkedIn URL'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Instagram URL'
            })
        }
        labels = {
            'name': 'Branch Name',
            'maps': 'Google Maps Link',
            'image': 'Branch Image',
            'description': 'Description',
            'address': 'Address',
            'email': 'Email Address',
            'office_open': 'Office Hours',
            'status': 'Active Status',
            'facebook': 'Facebook URL',
            'twitter': 'Twitter/X URL',
            'linkedin': 'LinkedIn URL',
            'instagram': 'Instagram URL'
        }
        help_texts = {
            'facebook': 'Leave as default or enter custom Facebook URL',
            'twitter': 'Leave as default or enter custom Twitter/X URL',
            'linkedin': 'Leave as default or enter custom LinkedIn URL',
            'instagram': 'Leave as default or enter custom Instagram URL',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Populate phone numbers from existing instance
            phone_numbers = self.instance.get_phone_numbers()
            self.fields['phone_numbers'].initial = ', '.join(phone_numbers)
    
    def clean_phone_numbers(self):
        phone_numbers = self.cleaned_data.get('phone_numbers', '')
        if phone_numbers:
            # Split by comma and validate each phone number
            numbers_list = [num.strip() for num in phone_numbers.split(',') if num.strip()]
            for number in numbers_list:
                if len(number) < 5:
                    raise forms.ValidationError(f"Phone number '{number}' is too short.")
        return phone_numbers
    
    def save(self, commit=True):
        branch = super().save(commit=False)
        
        # Handle phone numbers
        phone_numbers = self.cleaned_data.get('phone_numbers', '')
        if phone_numbers:
            numbers_list = [num.strip() for num in phone_numbers.split(',') if num.strip()]
            branch.set_phone_numbers(numbers_list)
        else:
            branch.phone = ''
        
        if commit:
            branch.save()
        return branch