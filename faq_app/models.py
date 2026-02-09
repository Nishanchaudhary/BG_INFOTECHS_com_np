from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import re

class FAQ(models.Model):
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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use this instead of direct User reference
        on_delete=models.CASCADE,
        related_name='faqs'
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Ordering
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'faq'
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return self.question
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
            # Ensure slug uniqueness
            counter = 1
            original_slug = self.slug
            while FAQ.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        
        if not self.meta_title:
            self.meta_title = self.question
        
        if not self.meta_description and self.answer:
            # Create meta description from first 160 chars of answer
            plain_text = self.answer.replace('<br>', ' ').replace('</p>', ' ')
            plain_text = re.sub('<[^<]+?>', '', plain_text)
            self.meta_description = plain_text[:160] + '...' if len(plain_text) > 160 else plain_text
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('faq_app:faq_detail', kwargs={'slug': self.slug})
    
# =============================================================================
# SLIDERS
# =============================================================================
# Your existing FAQ model remains the same...

class SliderManager(models.Manager):
    """Custom manager for Slider model"""
    
    def active(self):
        """Return only active sliders"""
        return self.filter(status=Slider.Status.ACTIVE)
    
    def get_ordered_active(self):
        """Return active sliders with ordering"""
        return self.active().order_by('order', '-created_at')


class Slider(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
    
    class Meta:
        db_table = 'slider'
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['status', 'order']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_slider_title',
                condition=models.Q(status='active')
            )
        ]

    # Required fields
    title = models.CharField(
        _('Title'),
        max_length=255,
        help_text=_('Enter a descriptive title for the slider (max 255 characters)')
    )
    
    short_description = models.TextField(
        _('Short Description'),
        max_length=500,
        help_text=_('Brief description of the slider content (max 500 characters)')
    )
    
    image = models.ImageField(
        _('Image'),
        upload_to='sliders/%Y/%m/%d/',
        help_text=_('Upload slider image (recommended size: 1200x600px)')
    )
    
    link = models.URLField(
        _('Link'),
        max_length=500,
        blank=True,
        null=True,
        help_text=_('Optional URL link for the slider')
    )
    
    # Status field with better implementation
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=Status.choices,
        default=Status.INACTIVE,
        help_text=_('Slider status')
    )
    
    # Additional fields for production
    order = models.PositiveIntegerField(
        _('Display Order'),
        default=0,
        help_text=_('Order in which sliders are displayed (lower numbers first)')
    )
    
    target_blank = models.BooleanField(
        _('Open in new tab'),
        default=False,
        help_text=_('Check to open link in new tab/window')
    )
    
    start_date = models.DateTimeField(
        _('Start Date'),
        blank=True,
        null=True,
        help_text=_('Date when slider becomes active')
    )
    
    end_date = models.DateTimeField(
        _('End Date'),
        blank=True,
        null=True,
        help_text=_('Date when slider becomes inactive')
    )
    
    # Audit fields
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='sliders_created'
    )
    
    objects = SliderManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('faq_app:slider_detail', kwargs={'pk': self.pk})

    @property
    def is_currently_active(self):
        """Check if slider is currently active based on dates"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.status != self.Status.ACTIVE:
            return False
            
        if self.start_date and self.start_date > now:
            return False
            
        if self.end_date and self.end_date < now:
            return False
            
        return True

    def clean(self):
        """Custom validation"""
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError({
                'end_date': _('End date must be after start date.')
            })
        
        # Check for unique active title
        if self.status == self.Status.ACTIVE:
            existing = Slider.objects.filter(
                title=self.title, 
                status=Slider.Status.ACTIVE
            ).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError({
                    'title': _('An active slider with this title already exists.')
                })

    def save(self, *args, **kwargs):
        """Override save to add custom logic"""
        self.full_clean()
        super().save(*args, **kwargs)