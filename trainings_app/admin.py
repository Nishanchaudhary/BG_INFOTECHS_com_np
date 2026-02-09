from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Training, TrainingImage

# Training Image Inline
class TrainingImageInline(admin.TabularInline):
    model = TrainingImage
    extra = 1
    fields = ['image', 'image_preview', 'status', 'order', 'created_at']
    readonly_fields = ['image_preview', 'created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'

# Training Admin
@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'image_preview',
        'duration_display',
        'price_display', 
        'offer_price_display',
        'discount_badge',
        'status',
        'images_count',
        'created_at'
    ]
    list_filter = [
        'status',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'title',
        'description'
    ]
    list_editable = ['status']
    readonly_fields = [
        'created_at',
        'updated_at',
        'image_preview_large',
        'discount_percentage_display',
        'images_count_display'
    ]
    date_hierarchy = 'created_at'
    inlines = [TrainingImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'duration',
                'description',
            )
        }),
        ('Pricing', {
            'fields': (
                'price',
                'offer_price',
                'discount_percentage_display',
            )
        }),
        ('Media', {
            'fields': (
                'image',
                'image_preview_large',
            )
        }),
        ('Settings', {
            'fields': (
                'status',
            )
        }),
        ('Statistics', {
            'fields': (
                'images_count_display',
                'created_at',
                'updated_at'
            )
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return format_html('<span class="text-muted">No Image</span>')
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="150" style="object-fit: cover; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" /><br><small>{}</small>',
                obj.image.url,
                obj.image.name
            )
        return "No image uploaded"
    image_preview_large.short_description = 'Image Preview'
    
    def duration_display(self, obj):
        # Convert duration to readable format
        total_seconds = int(obj.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"
    duration_display.short_description = 'Duration'
    
    def price_display(self, obj):
        # Format number with commas outside of format_html
        formatted_price = "{:,}".format(obj.price)
        return format_html(
            '<span style="color: #6c757d; text-decoration: line-through;">₹{}</span>',
            formatted_price
        )
    price_display.short_description = 'Original Price'
    
    def offer_price_display(self, obj):
        if obj.has_offer:
            # Format number with commas outside of format_html
            formatted_offer_price = "{:,}".format(obj.offer_price)
            return format_html(
                '<strong style="color: #28a745;">₹{}</strong>',
                formatted_offer_price
            )
        # Format number with commas outside of format_html
        formatted_price = "{:,}".format(obj.price)
        return format_html(
            '<strong>₹{}</strong>',
            formatted_price
        )
    offer_price_display.short_description = 'Current Price'
    
    def discount_badge(self, obj):
        if obj.has_offer:
            return format_html(
                '<span class="badge bg-danger">{}% OFF</span>',
                obj.discount_percentage
            )
        return format_html('<span class="badge bg-secondary">No Offer</span>')
    discount_badge.short_description = 'Discount'
    
    def images_count(self, obj):
        count = obj.images.count()
        url = reverse('admin:trainings_app_trainingimage_changelist') + f'?training__id__exact={obj.id}'
        return format_html(
            '<a href="{}" class="badge bg-info">{}</a>',
            url,
            count
        )
    images_count.short_description = 'Images'
    
    def images_count_display(self, obj):
        count = obj.images.count()
        active_count = obj.images.filter(status=True).count()
        inactive_count = obj.images.filter(status=False).count()
        return format_html(
            '''
            <div>
                <strong>Total:</strong> {}<br>
                <strong>Active:</strong> <span class="text-success">{}</span><br>
                <strong>Inactive:</strong> <span class="text-warning">{}</span>
            </div>
            ''',
            count, active_count, inactive_count
        )
    images_count_display.short_description = 'Images Statistics'
    
    def discount_percentage_display(self, obj):
        if obj.has_offer:
            # Format savings amount with commas outside of format_html
            savings = obj.price - obj.offer_price
            formatted_savings = "{:,}".format(savings)
            return format_html(
                '<div style="background: #d4edda; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745;">'
                '<strong>Discount:</strong> <span class="badge bg-danger" style="font-size: 14px;">{}% OFF</span><br>'
                '<small>You save: ₹{}</small>'
                '</div>',
                obj.discount_percentage,
                formatted_savings
            )
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 5px; border-left: 4px solid #6c757d;">'
            '<span class="text-muted">No active discount</span>'
            '</div>'
        )
    discount_percentage_display.short_description = 'Discount Information'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images')
    
    def save_model(self, request, obj, form, change):
        try:
            # Validate that offer price is not greater than original price
            if obj.offer_price > obj.price:
                messages.error(request, 'Offer price cannot be greater than original price!')
                return
            
            super().save_model(request, obj, form, change)
            messages.success(request, f'Training "{obj.title}" was saved successfully!')
            
        except Exception as e:
            messages.error(request, f'Error saving training: {str(e)}')

# Training Image Admin
@admin.register(TrainingImage)
class TrainingImageAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview',
        'training_link',
        'status',
        'order',
        'created_at'
    ]
    list_filter = [
        'status',
        'training',
        'created_at'
    ]
    search_fields = [
        'training__title'
    ]
    list_editable = ['status', 'order']
    readonly_fields = [
        'created_at',
        'image_preview_large'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Image Information', {
            'fields': (
                'training',
                'image',
                'image_preview_large',
            )
        }),
        ('Display Settings', {
            'fields': (
                'status',
                'order',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
            )
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return format_html('<span class="text-muted">No Image</span>')
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="150" style="object-fit: cover; border: 1px solid #ddd; border-radius: 5px; padding: 5px;" /><br><small>{}</small>',
                obj.image.url,
                obj.image.name
            )
        return "No image uploaded"
    image_preview_large.short_description = 'Image Preview'
    
    def training_link(self, obj):
        url = reverse('admin:trainings_app_training_change', args=[obj.training.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.training.title
        )
    training_link.short_description = 'Training'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('training')

# Custom Actions
def activate_trainings(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    messages.success(request, f'Successfully activated {updated} training(s).')
activate_trainings.short_description = "Activate selected trainings"

def deactivate_trainings(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    messages.success(request, f'Successfully deactivated {updated} training(s).')
deactivate_trainings.short_description = "Deactivate selected trainings"

def activate_images(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    messages.success(request, f'Successfully activated {updated} image(s).')
activate_images.short_description = "Activate selected images"

def deactivate_images(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    messages.success(request, f'Successfully deactivated {updated} image(s).')
deactivate_images.short_description = "Deactivate selected images"

# Add custom actions to models
TrainingAdmin.actions = [activate_trainings, deactivate_trainings]
TrainingImageAdmin.actions = [activate_images, deactivate_images]

# Admin site customization
admin.site.site_header = 'BG INFOTECHS'
admin.site.site_title = 'BG Infotechs Admin'
admin.site.index_title = 'BG Infotechs Administration'