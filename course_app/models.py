from django.db import models
from django.conf import settings

MEDIA_TYPE_CHOICES = [
    ('image', 'Image'),
    ('video', 'Video'),
]

class Course(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='course_img/')
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    duration = models.DurationField()
    price = models.PositiveIntegerField()
    offer_price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    
    # Make sure this author field exists and points to your custom User model
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='courses'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_actual_price(self):
        """Return the actual price (offer price if available, else regular price)"""
        return self.offer_price if self.offer_price and self.offer_price < self.price else self.price
    
    def has_discount(self):
        """Check if course has discount"""
        return self.offer_price and self.offer_price < self.price
    
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.has_discount():
            return int(((self.price - self.offer_price) / self.price) * 100)
        return 0
    
    def duration_display(self):
        """Format duration for display"""
        total_seconds = int(self.duration.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        
        if days > 0:
            return f"{days} day{'s' if days > 1 else ''} {hours} hour{'s' if hours > 1 else ''}"
        elif hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            return f"{minutes} minute{'s' if minutes > 1 else ''}"
        
    @property
    def enrollment_count(self):
        """Return the number of active enrollments for this course"""
        return self.enrollments.filter(status=True).count()
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']

class Media(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='media',
        null=False,
        blank=False
    )
    media_type = models.CharField(
        max_length=10, 
        choices=MEDIA_TYPE_CHOICES
    )
    file = models.FileField(upload_to='course_media/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.media_type} for {self.course.title}"
    
    def file_type_icon(self):
        """Return appropriate icon based on media type"""
        if self.media_type == 'image':
            return 'fas fa-image'
        elif self.media_type == 'video':
            return 'fas fa-video'
        return 'fas fa-file'
    
    def active_media_count(self):
        return self.media.filter(status=True).count()

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ['order', 'created_at']

# Course Enrollment Model
class CourseEnrollment(models.Model):
    # Define choices at the class level
    EDUCATION_CHOICES = [
        ('high_school', 'High School Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]

    EXPERIENCE_CHOICES = [
        ('none', 'No Experience'),
        ('less_than_1_year', 'Beginner (Less than 1 year)'),
        ('1_3_years', 'Intermediate (1-3 years)'),
        ('3_5_years', 'Advanced (3-5 years)'),
        ('more_than_5_years', 'Expert (More than 5 years)'),
    ]

    SOURCE_CHOICES = [
        ('friend', 'Friend/Colleague'),
        ('social_media', 'Social Media'),
        ('website', 'Website'), 
        ('other', 'Other'),
    ]

    # Course and Student Information
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    
    # Education field - FIXED: Use models.CharField with choices parameter
    education = models.CharField(
        max_length=20, 
        choices=EDUCATION_CHOICES,
        blank=True,
        null=True
    )
    
    # Experience field - FIXED: Use models.CharField with choices parameter
    experience = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_CHOICES,
        blank=True,
        null=True
    )
    
    # How did you hear about us?
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True
    )
    
    # Timestamps and status
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} enrolled in {self.course.title}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        ordering = ['-enrolled_at']