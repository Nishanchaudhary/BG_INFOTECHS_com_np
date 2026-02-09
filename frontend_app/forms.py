from django import forms
from package_app.models import PlanSubscriber, CustomPackage
from contact_app.models import Contact
from company_app.models import Services

class PlanSubscriberForm(forms.ModelForm):
    class Meta:
        model = PlanSubscriber
        fields = ['name_business_name', 'phone_number', 'email', 'package']
        widgets = {
            'name_business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name/business name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'package': forms.Select(attrs={'class': 'form-control',
                                           'placeholder':'Package'
                                           })
        }

class CustomPackageForm(forms.ModelForm):
    # Add choices for the select fields
    BUSINESS_CATEGORY_CHOICES = [
        ('', 'Choose a Category'),
        ('Consultancy', 'Consultancy'),
        ('Healthcare', 'Hospitals and Healthcare'),
        ('Travel', 'Travels and Trekking'),
        ('Education', 'Educational Institutional'),
        ('E-Commerce', 'E-Commerce'),
        ('Other', 'Others'),
    ]
    
    GRAPHICS_CHOICES = [
        ('', 'Select no. of Graphics'),
        ('1-14', '1 - 14'),
        ('14-20', '14 - 20'),
        ('20-25', '20 - 25'),
        ('25+', '25+'),
    ]
    
    VIDEOS_CHOICES = [
        ('', 'Select no. of videos/GIFs'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4+', '4+'),
    ]
    
    business_category = forms.ChoiceField(
        choices=BUSINESS_CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    no_of_graphics = forms.ChoiceField(
        choices=GRAPHICS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    no_of_videos = forms.ChoiceField(
        choices=VIDEOS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = CustomPackage
        fields = ['name_business_name', 'phone_number', 'email', 'business_category', 'no_of_graphics', 'no_of_videos']
        widgets = {
            'name_business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose your name or business name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
        }


class ContactForm(forms.ModelForm):
    newsletter_subscription = forms.BooleanField(
        required=False,
        initial=True,
        label="Yes, I'd like to receive occasional updates and relevant news from BG-Infotechs."
    )
    
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone_number', 'service', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'e.g., John Doe',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'e.g., john@example.com',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g., +977 98XXXXXXXX',
                'class': 'form-control'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project or inquiry...',
                'rows': 5,
                'class': 'form-control'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'service': 'Select Service',
            'message': 'Message'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show all services without filtering by is_active
        self.fields['service'].queryset = Services.objects.all()
        self.fields['service'].empty_label = "Choose a service"