from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
import math

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
        help_text=_("Enter a descriptive title for the blog post (5-100 characters)")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_("URL-friendly version of the title")
    )
    image = models.ImageField(
        upload_to='blog_images/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text=_("Upload a featured image for the blog post")
    )
    short_description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Brief summary of the blog post (max 255 characters)")
    )
    description = models.TextField(
        validators=[MinLengthValidator(50)],
        help_text=_("Main content of the blog post")
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['slug']),
        ]
    
    def get_absolute_url(self):
        return reverse('frontend_app:blog_details', args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if self.status == Blog.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        return self.status == Blog.Status.PUBLISHED
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        try:
            # Safely strip HTML tags and count words
            plain_text = strip_tags(self.description or '')
            word_count = len(plain_text.split())
            reading_time = math.ceil(word_count / 200)  # 200 words per minute
            return max(1, reading_time)  # At least 1 minute
        except:
            return 1  # Default to 1 minute if there's any error

class BlogComment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    full_name = models.CharField(max_length=100, default='full name')
    email = models.EmailField(default='your email')
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text=_("Enter your comment (minimum 10 characters)")
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog Comment")
        verbose_name_plural = _("Blog Comments")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['blog', 'status', 'created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.email} on {self.blog.title}"
    
    @property
    def is_approved(self):
        return self.status == BlogComment.Status.APPROVED