from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Company_profile, Features, Services, Testimonials, 
    Project_done, Services_testimonial, Services_faq,Services_success
)

# Admin site customization
admin.site.site_header = "BG Infotechs Administration"
admin.site.site_title = "BG Infotechs Admin Portal"
admin.site.index_title = "Welcome to BG Infotechs Admin Portal"

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_email', 'company_phone', 'display_logo', 'display_favicon']
    list_filter = ['company_name']
    search_fields = ['company_name', 'company_email', 'company_phone']
    readonly_fields = ['display_logo', 'display_footer_logo', 'display_favicon', 'display_company_image']
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'company_email', 'company_phone', 'company_address')
        }),
        ('Media Files', {
            'fields': ('company_logo', 'display_logo', 'company_footer_logo', 'display_footer_logo', 
                      'company_favicon', 'display_favicon', 'company_image', 'display_company_image')
        }),
        ('Company Content', {
            'fields': ('company_intro', 'company_mission', 'company_vision', 'company_footer', 'map_iframe')
        }),
        ('Social Media Links', {
            'fields': ('facebook_link', 'instagram_link', 'twitter_link', 'youtube_link'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def display_logo(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.company_logo.url)
        return "No Logo"
    display_logo.short_description = 'Logo Preview'
    
    def display_footer_logo(self, obj):
        if obj.company_footer_logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.company_footer_logo.url)
        return "No Footer Logo"
    display_footer_logo.short_description = 'Footer Logo Preview'
    
    def display_favicon(self, obj):
        if obj.company_favicon:
            return format_html('<img src="{}" width="32" height="32" />', obj.company_favicon.url)
        return "No Favicon"
    display_favicon.short_description = 'Favicon Preview'
    
    def display_company_image(self, obj):
        if obj.company_image:
            return format_html('<img src="{}" width="100" height="100" style="border-radius: 5px;" />', obj.company_image.url)
        return "No Company Image"
    display_company_image.short_description = 'Company Image Preview'
    
    def has_add_permission(self, request):
        # Allow only one company profile
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_icon', 'status', 'tags_preview']
    list_filter = ['status']
    search_fields = ['title', 'description', 'tags']
    list_editable = ['status']
    readonly_fields = ['tags_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('tags', 'tags_preview', 'status')
        }),
    )
    
    def display_icon(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 20px;"></i>', obj.icon)
        return "No Icon"
    display_icon.short_description = 'Icon'
    
    def tags_preview(self, obj):
        if obj.tags:
            tags_list = obj.get_tags_list()
            badges = ''.join([f'<span class="badge bg-secondary me-1">{tag}</span>' for tag in tags_list])
            return format_html(badges)
        return "No Tags"
    tags_preview.short_description = 'Tags Preview'

class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_title', 'display_image', 'status']
    list_filter = ['status']
    search_fields = ['title', 'sub_title', 'description']
    list_editable = ['status']
    readonly_fields = ['display_image']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'sub_title', 'description')
        }),
        ('Media', {
            'fields': ('image', 'display_image', 'icon')
        }),
        ('Settings', {
            'fields': ('status',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image Preview'

@admin.register(Services_success)
class ServicesSuccessAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'success', 'status')
    list_filter = ('status', 'service')
    search_fields = ('title', 'success', 'service__title')
    ordering = ('service', 'title')
    list_editable = ('status',)
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'icon', 'service', 'success')
        }),
        ('Status', {
            'fields': ('status',),
        }),
    )

    # Optional: display a more readable object name
    def __str__(self, obj):
        return f"{obj.title} - {obj.service.title}"




class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'display_image', 'rating_stars', 'status']
    list_filter = ['status', 'rating']
    search_fields = ['name', 'designation', 'message']
    list_editable = ['status']
    readonly_fields = ['display_image', 'rating_stars_display']
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'designation', 'image', 'display_image')
        }),
        ('Testimonial Content', {
            'fields': ('message', 'rating', 'rating_stars_display')
        }),
        ('Settings', {
            'fields': ('status',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Client Photo'
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return stars
    rating_stars.short_description = 'Rating'
    
    def rating_stars_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 16px;">{}</span>', stars)
    rating_stars_display.short_description = 'Rating Display'

class ProjectDoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'service', 'display_image', 'display_logo', 'status', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['title', 'company', 'description', 'service__title']
    list_editable = ['status']
    readonly_fields = ['display_image', 'display_logo', 'created_at', 'updated_at']
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'service', 'company', 'description')
        }),
        ('Media Files', {
            'fields': ('image', 'display_image', 'logo', 'display_logo')
        }),
        ('Project Links', {
            'fields': ('live_link',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Project Image'
    
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: contain; border-radius: 5px;" />', obj.logo.url)
        return "No Logo"
    display_logo.short_description = 'Company Logo'

class ServicesTestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'service', 'designation', 'display_image', 'rating_stars', 'status', 'created_at']
    list_filter = ['status', 'rating', 'service', 'created_at']
    search_fields = ['name', 'designation', 'message', 'service__title']
    list_editable = ['status']
    readonly_fields = ['display_image', 'rating_display', 'short_message_display', 'created_at', 'updated_at']
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'designation', 'image', 'display_image')
        }),
        ('Service & Testimonial', {
            'fields': ('service', 'message', 'short_message_display', 'rating', 'rating_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Client Photo'
    
    def rating_stars(self, obj):
        return obj.star_display
    rating_stars.short_description = 'Rating'
    
    def rating_display(self, obj):
        return format_html('<span style="font-size: 16px;">{}</span>', obj.star_display)
    rating_display.short_description = 'Rating Display'
    
    def short_message_display(self, obj):
        return format_html('<em>{}</em>', obj.short_message)
    short_message_display.short_description = 'Message Preview'

class ServicesFaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'service', 'status_badge', 'created_at', 'updated_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['question', 'answer', 'service__title']
    list_editable = ['service']
    readonly_fields = ['status_badge_display', 'slug', 'created_at', 'updated_at', 'answer_preview']
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'slug', 'answer', 'answer_preview')
        }),
        ('Service & Status', {
            'fields': ('service', 'status', 'status_badge_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        color_map = {
            'draft': 'secondary',
            'published': 'success',
            'archived': 'warning'
        }
        color = color_map.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def status_badge_display(self, obj):
        return self.status_badge(obj)
    status_badge_display.short_description = 'Current Status'
    
    def answer_preview(self, obj):
        preview = obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer
        return format_html('<div style="background: #f8f9fa; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff;"><em>{}</em></div>', preview)
    answer_preview.short_description = 'Answer Preview'

# Register all models with their admin classes
admin.site.register(Company_profile, CompanyProfileAdmin)
admin.site.register(Features, FeaturesAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Project_done, ProjectDoneAdmin)
admin.site.register(Services_testimonial, ServicesTestimonialAdmin)
admin.site.register(Services_faq, ServicesFaqAdmin)

