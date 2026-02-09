from django.db import models
from company_app.models import Services

class Branch(models.Model):
    name = models.CharField(max_length=255)
    maps = models.CharField(max_length=500)
    image = models.ImageField(upload_to='branch_img')
    description = models.TextField()
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, help_text="Enter multiple phone numbers separated by commas")
    email = models.EmailField()
    office_open = models.CharField(max_length=255)
    status = models.BooleanField()
    facebook = models.URLField(default='https://www.facebook.com/')
    twitter = models.URLField(default='https://www.x.com/')
    linkedin = models.URLField(default='https://www.linkedin.com/')
    instagram = models.URLField(default='https://www.instagram.com/')

    def get_phone_numbers(self):
        """Returns a list of phone numbers"""
        if self.phone:
            return [phone.strip() for phone in self.phone.split(',')]
        return []
    
    def set_phone_numbers(self, phone_list):
        """Sets phone numbers from a list"""
        self.phone = ', '.join([str(phone).strip() for phone in phone_list])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Branches"

class Contact(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]

    full_name = models.CharField(
        max_length=100,
        help_text="Enter your full name"
    )
    email = models.EmailField(
        help_text="Enter your email address"
    )
    phone_number = models.CharField(
        max_length=20,
        help_text="Enter phone number with country code"
    )
    message = models.TextField(
        help_text="Enter your message"
    )
   
    service = models.ForeignKey(
        'company_app.Services', 
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text="Select the service you're inquiring about"
    )
    status = models.BooleanField(
        choices=STATUS_CHOICES,
        default=True,
        help_text="Contact status"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Mark as read"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this contact was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this contact was last updated"
    )

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
      

    def __str__(self):
        return f"{self.full_name} - {self.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def mark_as_read(self):
        """Mark the contact as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])

    def mark_as_unread(self):
        """Mark the contact as unread"""
        self.is_read = False
        self.save(update_fields=['is_read'])

    def get_short_message(self, length=50):
        """Get truncated message for display"""
        if len(self.message) <= length:
            return self.message
        return self.message[:length] + '...'

    @classmethod
    def get_unread_count(cls):
        """Get count of unread messages"""
        return cls.objects.filter(is_read=False).count()

    def save(self, *args, **kwargs):
        # Auto-capitalize full name
        if self.full_name:
            self.full_name = ' '.join([name.capitalize() for name in self.full_name.split()])  
        super().save(*args, **kwargs)