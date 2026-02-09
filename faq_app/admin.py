from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import FAQ, Slider

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'slug', 'status', 'display_order', 'author', 'created_at']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['question', 'answer', 'slug']
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    prepopulated_fields = {'slug': ('question',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('question', 'answer', 'slug', 'status')
        }),
        ('SEO Information', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('display_order',)
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = [
        'title_preview', 
        'image_thumbnail', 
        'status_badge', 
        'current_status', 
        'order', 
        'created_by', 
        'created_at_formatted'
    ]
    list_filter = ['status', 'created_at', 'created_by', 'target_blank']
    search_fields = ['title', 'short_description', 'link']
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'current_status_display']
    list_editable = ['order']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'short_description', 'image', 'image_preview')
        }),
        ('Link Settings', {
            'fields': ('link', 'target_blank')
        }),
        ('Status & Display', {
            'fields': ('status', 'order')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        ('Current Status', {
            'fields': ('current_status_display',),
            'classes': ('collapse',)
        }),
        ('Author Information', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_preview(self, obj):
        """Display truncated title with description"""
        title = obj.title[:50] + "..." if len(obj.title) > 50 else obj.title
        desc = obj.short_description[:80] + "..." if len(obj.short_description) > 80 else obj.short_description
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            title,
            desc
        )
    title_preview.short_description = 'Title & Description'
    
    def image_thumbnail(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 40px; object-fit: cover; border-radius: 4px;">',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = 'Image'
    
    def image_preview(self, obj):
        """Display larger image preview in edit view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 150px; border-radius: 8px;">',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = 'Image Preview'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        color = 'green' if obj.status == 'active' else 'gray'
        text = 'Active' if obj.status == 'active' else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            text
        )
    status_badge.short_description = 'Status'
    
    def current_status(self, obj):
        """Display current active status"""
        if obj.is_currently_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">● Active</span>'
            )
        return format_html(
            '<span style="color: gray;">● Inactive</span>'
        )
    current_status.short_description = 'Current'
    
    def current_status_display(self, obj):
        """Display detailed current status in edit view"""
        if obj.is_currently_active:
            return format_html(
                '<div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; border: 1px solid #c3e6cb;">'
                '<strong>✓ Currently Active</strong><br>'
                '<small>This slider is currently visible to users.</small>'
                '</div>'
            )
        else:
            reasons = []
            if obj.status != 'active':
                reasons.append("Status is not set to 'Active'")
            if obj.start_date and obj.start_date > timezone.now():
                reasons.append("Start date is in the future")
            if obj.end_date and obj.end_date < timezone.now():
                reasons.append("End date has passed")
            
            reason_text = " | ".join(reasons) if reasons else "Slider is inactive"
            return format_html(
                '<div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; border: 1px solid #f5c6cb;">'
                '<strong>✗ Currently Inactive</strong><br>'
                '<small>{}</small>'
                '</div>',
                reason_text
            )
    current_status_display.short_description = 'Current Status Details'
    
    def created_at_formatted(self, obj):
        """Format created date"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_formatted.short_description = 'Created'
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new slider"""
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        """Make created_by readonly after creation"""
        if obj and obj.created_by:
            return self.readonly_fields + ['created_by']
        return self.readonly_fields