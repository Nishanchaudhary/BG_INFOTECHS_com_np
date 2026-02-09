from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class JobType(models.TextChoices):
    FULL_TIME = 'full_time', 'Full Time'
    PART_TIME = 'part_time', 'Part Time'
    HYBRID = 'hybrid', 'Hybrid'
    REMOTE = 'remote', 'Remote'

class Vacancy(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        DRAFT = 'draft', 'Draft'
    
    title = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME
    )
    image = models.ImageField(upload_to='vacancy_images/')
    address = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField(help_text="Enter skills separated by commas")
    salary = models.CharField(max_length=50)
    expired_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    
    # Audit fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacancies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []
    
    def is_expired(self):
        """Check if the vacancy has expired"""
        return self.expired_date < timezone.now().date()
    
    def is_active(self):
        """Check if vacancy is active and not expired"""
        return self.status == self.Status.ACTIVE and not self.is_expired()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"
        ordering = ['-created_at']

class JobApplication(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        REVIEWED = 'reviewed', 'Reviewed'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    
    # Applicant details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    
    # Application metadata
    status = models.CharField(
        max_length=10,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.vacancy.title}"
    
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-applied_at']
        unique_together = ['vacancy', 'email']  # Prevent duplicate applications