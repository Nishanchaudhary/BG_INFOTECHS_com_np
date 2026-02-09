from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
import os
# Create your models here.

class Company_profile(models.Model):
    company_name = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=15, null=True, blank=True)
    company_address = models.CharField(max_length=100, null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    company_footer_logo = models.ImageField(upload_to='company_footer_logos/', null=True, blank=True)
    company_favicon = models.ImageField(upload_to='company_favicons/', null=True, blank=True)
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)
    company_intro = models.TextField(null=True, blank=True)
    company_mission = models.TextField(null=True, blank=True)
    company_vision = models.TextField(null=True, blank=True)
    company_footer = models.TextField(null=True, blank=True)
    map_iframe = models.TextField(null=True, blank=True)

    # social media links
    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    # SEO fields
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(("Meta Keywords"), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name
    class Meta:
        permissions = [
            ("manage_company_profile", "Can manage company profile"),
        ]
# Features Model...........
class Features(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(max_length=200, blank=True)  
    icon = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []
    
    def set_tags(self, tags_list):
        self.tags = ','.join(tags_list)
    
    def __str__(self):
        return self.title

# Services Model...........  
class Services(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    

    def clean(self):
        if len(self.title) < 2:
            raise ValidationError({'title': 'Title must be at least 2 characters long.'})
        if len(self.description) < 10:
            raise ValidationError({'description': 'Description must be at least 10 characters long.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['title']


class Services_success(models.Model):
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(
        Services, 
        on_delete=models.CASCADE,
        verbose_name="Service",
        help_text="Select a service from the dropdown"
    )
    success = models.CharField(max_length=50)
    status = models.BooleanField()
    

    def __str__(self):
        return self.title

    def clean(self):
        """Validation for success model"""
        if len(self.title.strip()) < 2:
            raise ValidationError({'title': 'Title must be at least 2 characters long.'})

    def save(self, *args, **kwargs):
        """Validate before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.service.title}"


# Testimonials Model
class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# Catagory...............................................................
class Category(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text="Category name (e.g., Web Development, Mobile Apps)"
    )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="URL-friendly version of the title (auto-generated)"
    )
    
    image = models.ImageField(
        upload_to='category/images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Category thumbnail image"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Brief description of the category"
    )
    
    status = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Whether the category is active and visible"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Date"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    ordering = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Higher number appears first"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-ordering', 'title']
        db_table = 'categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    @property
    def is_active(self):
        return self.status

    def get_image_url(self):
        """Return image URL or default if not available"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/default-category.png' 

# Project done.................   
class Project_done(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="project_done/")
    service = models.ForeignKey(
        Services, 
        on_delete=models.CASCADE,
        verbose_name="Service",
        help_text="Select a service from the dropdown"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        verbose_name="category",
        null=True,
        blank=True,
        help_text="Select a category from the dropdown"
    )

    company = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="company_logo/")
    description = models.TextField()
    live_link = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def clean(self):
        if len(self.title) < 2:
            raise ValidationError({'title': 'Title must be at least 2 characters long.'})
        if len(self.description) < 10:
            raise ValidationError({'description': 'Description must be at least 10 characters long.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.logo:
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.company}"

    class Meta:
        verbose_name = 'Project Done'
        verbose_name_plural = 'Projects Done'
        ordering = ['-created_at']

# Services_testimonial...........................................................
class Services_testimonial(models.Model):
    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )
    
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name="Client Name",
        help_text="Enter the full name of the client"
    )
    designation = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name="Designation/Position",
        help_text="Client's job title or position (optional)"
    )
    image = models.ImageField(
        upload_to='services_testimonials/%Y/%m/%d/',
        null=True, 
        blank=True,
        verbose_name="Client Photo",
        help_text="Upload client's photo (recommended: 200x200px)"
    )
    service = models.ForeignKey(
        Services, 
        on_delete=models.CASCADE,
        verbose_name="Service",
        help_text="Select the service this testimonial is for"
    )
    message = models.TextField(
        verbose_name="Testimonial Message",
        help_text="Share the client's experience and feedback"
    )
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name="Rating",
        help_text="Select client's satisfaction rating"
    )
    status = models.BooleanField(
        choices=STATUS_CHOICES,
        default=True,
        verbose_name="Status",
        help_text="Toggle to show/hide testimonial"
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def clean(self):
        """Custom validation"""
        from django.core.exceptions import ValidationError
        
        # Name validation
        if len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Name must be at least 2 characters long.'})
        
        # Message validation
        if len(self.message.strip()) < 10:
            raise ValidationError({'message': 'Testimonial message must be at least 10 characters long.'})
        
        # Rating validation
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})

    def save(self, *args, **kwargs):
        """Override save to add validation"""
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete associated image file when object is deleted"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.service.title}"

    @property
    def star_display(self):
        """Return star rating for display"""
        return dict(self.RATING_CHOICES).get(self.rating, '')

    @property
    def short_message(self):
        """Return truncated message for listings"""
        if len(self.message) > 100:
            return self.message[:100] + '...'
        return self.message

    class Meta:
        verbose_name = 'Service Testimonial'
        verbose_name_plural = 'Service Testimonials'
        ordering = ['-created_at', 'service']
        indexes = [
            models.Index(fields=['service', 'status']),
            models.Index(fields=['rating']),
        ]

# Services_faq............................
class Services_faq(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    
    question = models.CharField(max_length=255)
    answer = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    service = models.ForeignKey(
        'Services', 
        on_delete=models.CASCADE,
        verbose_name="Service",
        help_text="Select the service this FAQ is for"
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
