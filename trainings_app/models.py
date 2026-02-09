from django.db import models

class Training(models.Model):  
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='training_images/', null=True, blank=True)  
    duration = models.DurationField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    offer_price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
 
    @property
    def has_offer(self):
        try:
            # Handle None values and ensure both are numbers
            if self.price is None or self.offer_price is None:
                return False
            return self.offer_price < self.price
        except (TypeError, ValueError):
            return False
 
    @property
    def discount_percentage(self):
        try:
            if self.has_offer and self.price and self.price > 0:
                discount = ((self.price - self.offer_price) / self.price) * 100
                return int(discount)
            return 0
        except (TypeError, ValueError, ZeroDivisionError):
            return 0

class TrainingImage(models.Model):  
    training = models.ForeignKey(
        Training, 
        on_delete=models.CASCADE, 
        related_name='images', 
        default=None
    )
    image = models.ImageField(upload_to='training_multi_images/', verbose_name='Image')
    status = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']  
    
    def __str__(self):
        return f"Image for {self.training.title}"