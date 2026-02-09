from django import forms
from .models import Features, Services,Testimonials,Project_done,Services_testimonial,Services_faq,Category,Services_success

# Features Form
class FeaturesForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter feature description...'
        }),
        required=False
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., UI, Mobile, Security)'
        }),
        help_text='Separate multiple tags with commas'
    )
    
    class Meta:
        model = Features
        fields = ['title', 'description', 'tags', 'icon', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter feature title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter feature description...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-cog, bi bi-feather'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }),
        }
        help_texts = {
            'icon': 'Enter Font Awesome or Bootstrap Icons class names',
            'status': 'Toggle to activate or deactivate this feature',
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return ','.join(tags_list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

#  Services Form 
class ServiceForm(forms.ModelForm):
    remove_image = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'})
    )
    
    class Meta:
        model = Services
        fields = ['title', 'sub_title', 'image', 'description', 'icon', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service title',
                'required': True
            }),
            'sub_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sub title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter detailed service description...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-cog'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'accept': 'image/*'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
        }
        labels = {
            'title': 'Service Title *',
            'sub_title': 'Sub Title',
            'image': 'Service Image',
            'description': 'Description *',
            'icon': 'Icon Class',
            'status': 'Active Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field not required for updates
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Service title is required.")
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Service description is required.")
        
        # Check text content length
        if len(description.strip()) < 10:
            raise forms.ValidationError("Description must contain at least 10 characters of text.")
        return description
    
    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon and not icon.startswith(('fas ', 'fab ', 'far ', 'fa-')):  # Basic Font Awesome validation
            raise forms.ValidationError("Please enter a valid Font Awesome icon class.")
        return icon
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle image removal
        if self.cleaned_data.get('remove_image') and instance.image:
            instance.image.delete(save=False)
            instance.image = None
        
        if commit:
            instance.save()
        return instance

class ServiceSuccessForm(forms.ModelForm):
    class Meta:
        model = Services_success
        fields = ['title', 'icon', 'service', 'success', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title (min 2 characters)'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter icon class (e.g., fas fa-check)'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'success': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter success value'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'title': 'Title must be at least 2 characters long.',
            'icon': 'Enter Font Awesome or other icon classes.',
            'success': 'Enter the success metric or value.',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 2:
            raise forms.ValidationError('Title must be at least 2 characters long.')
        return title


class ServiceSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search services by title, subtitle or description...',
            'id': 'search-input'
        })
    )
    
    status_filter = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Status'),
            ('active', 'Active Only'),
            ('inactive', 'Inactive Only'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'status-filter'
        })
    )

# Testimonials Form
class TestimonialForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter testimonial message...'
        })
    )
    
    class Meta:
        model = Testimonials
        fields = ['name', 'designation', 'image', 'message', 'rating', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter testimonial message...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'type': 'number'
            }),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long")
        return message

    
# Project Done.........................
class ProjectDoneForm(forms.ModelForm):
    class Meta:
        model = Project_done
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter project description...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'live_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image and logo not required for existing instances (edit)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
            self.fields['logo'].required = False
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not self.instance.pk and not image:  # Create operation
            raise forms.ValidationError('Project image is required.')
        return image
    
    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if not self.instance.pk and not logo:  # Create operation
            raise forms.ValidationError('Company logo is required.')
        return logo
     
# Services_Testimonial
class ServicesTestimonialForm(forms.ModelForm):
    class Meta:
        model = Services_testimonial
        fields = ['name', 'designation', 'image', 'service', 'message', 'rating', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter client name'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter client designation (optional)'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter testimonial message',
                'rows': 4
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field optional in form
        self.fields['image'].required = False
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        
# ServicesFaq...............................................

class ServicesFaqForm(forms.ModelForm):
    class Meta:
        model = Services_faq
        fields = ['question', 'answer', 'status', 'service', 'slug']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the FAQ question'
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter the FAQ answer'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'service': forms.Select(attrs={
                'class': 'form-control'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated slug (optional)'
            }),
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from question',
        }

# CategoryForm.................................................
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image', 'description', 'status', 'ordering']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter category description'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order (higher appears first)'
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Category.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A category with this title already exists.")
        return title