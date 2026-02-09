from django import forms
from django.forms import inlineformset_factory
from .models import Blog, BlogComment, Category

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'category', 'image', 'short_description', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL-friendly version'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of the blog post'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Main content of the blog post'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure category queryset is properly set
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a category (optional)"

class BlogCommentForm(forms.ModelForm):
#     class Meta:
#         model = BlogComment
#         fields = ['comment', 'status']
#         widgets = {
#             'comment': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter your comment...',
#                 'rows': 3
#             }),
#             'status': forms.Select(attrs={
#                 'class': 'form-control'
#             })
#         }

# BlogCommentFormSet = inlineformset_factory(
#     Blog,
#     BlogComment,
#     form=BlogCommentForm,
#     extra=1,
#     can_delete=True,
#     min_num=0,
#     validate_min=True
# )
    pass

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL-friendly version (auto-generated if empty)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter category description (optional)'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A category with this name already exists.')
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Category.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A category with this slug already exists.')
        return slug