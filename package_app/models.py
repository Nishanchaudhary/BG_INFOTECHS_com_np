from django.db import models
from django.utils import timezone

class Package(models.Model):
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='packages/', blank=True, null=True )
    month_price = models.PositiveIntegerField()
    year_price = models.PositiveIntegerField()
    short_desc = models.CharField(max_length=300)
    description = models.TextField()
    graphic_design = models.CharField(max_length=100)
    motion_graphic = models.CharField(max_length=100)
    shute_video = models.CharField(max_length=100)
    content_video = models.CharField(max_length=100)
    real = models.CharField(max_length=100)
    bosting = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    tags = models.CharField(max_length=500, blank=True, null=True )
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"

class PlanSubscriber(models.Model):
    name_business_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    created_at = models.DateTimeField( default=timezone.now )
    
    def __str__(self):
        return self.name_business_name
    class Meta:
        verbose_name = "Plan Subscriber"
        verbose_name_plural = "Plan Subscriber"


class CustomPackage(models.Model):
    name_business_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    business_category = models.CharField(max_length=200)
    no_of_graphics = models.CharField(max_length=100)
    no_of_videos = models.CharField(max_length=100)
    created_at = models.DateTimeField( default=timezone.now )
    
    def __str__(self):
        return self.name_business_name

    class Meta:
        verbose_name = "Custom Package"
        verbose_name_plural = "Custom Packages"
