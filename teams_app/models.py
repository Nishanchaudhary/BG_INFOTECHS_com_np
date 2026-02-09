from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Teams(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
    
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="teams/")
    phone = models.CharField(max_length=20)  # Changed to CharField for flexibility
    email = models.EmailField()
    
    # Social links
    facebook = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    
    # Skills as a TextField to store comma-separated values
    skills = models.TextField(help_text="Enter skills separated by commas")
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    display_order = models.IntegerField(default=0)
    
    # Audit fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['display_order', '-created_at']