from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db.models.signals import post_migrate, post_save, m2m_changed
from django.dispatch import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from course_app.models import Course  
class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='roles',
        help_text="Django permissions assigned to this role"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    # Add custom related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="bg_app_user_set",  # Custom related_name
        related_query_name="bg_app_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="bg_app_user_set",  # Custom related_name
        related_query_name="bg_app_user",
    )
    
    # Your custom fields
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    status = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
        permissions = [
            ("view_admin_dashboard", "Can view admin dashboard"),
            ("view_staff_dashboard", "Can view staff dashboard"),
            ("view_student_dashboard", "Can view student dashboard"),
            ("manage_staff", "Can manage staff"),
            ("manage_students", "Can manage students"),
            ("manage_financial", "Can manage financial data"),
            ("manage_roles", "Can manage roles"),
        ]
    
    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    enrollment_number = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=100)
    training = models.CharField(max_length=100)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_date = models.DateField(auto_now_add=True)
    training_end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.user.username} - {self.enrollment_number}"

    @property
    def fees_due(self):
        return self.total_fees - self.fees_paid

    @property
    def fees_paid_percentage(self):
        if self.total_fees > 0:
            return (self.fees_paid / self.total_fees) * 100
        return 0


class Staff(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='staff_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default='General')
    position = models.CharField(max_length=100, default='Staff')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    join_date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
        ordering = ['-join_date']

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"

    @property
    def salary_due(self):
        return self.salary - self.paid_salary

    @property
    def salary_paid_percentage(self):
        if self.salary > 0:
            return (self.paid_salary / self.salary) * 100
        return 0


class StaffPermission(models.Model):
    """Model to manage staff permissions separately using Django permissions"""
    staff_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role__name': 'staff'},
        related_name='staff_permissions'
    )
    django_permissions = models.ManyToManyField(
        Permission, 
        blank=True,
        help_text="Specific Django permissions for this staff member"
    )
    groups = models.ManyToManyField(
        Group, 
        blank=True,
        help_text="Django groups for this staff member"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Staff Permission"
        verbose_name_plural = "Staff Permissions"
    
    def __str__(self):
        return f"Permissions for {self.staff_user.username}"