from django.contrib import admin
from django.utils.html import format_html
from .models import Teams

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'display_image', 
        'designation', 
        'email', 
        'phone', 
        'status', 
        'display_order',
        'created_at',
        'author'
    ]
    
    list_filter = [
        'status',
        'designation',
        'created_at',
        'author'
    ]
    
    search_fields = [
        'name',
        'email',
        'phone',
        'designation',
        'description'
    ]
    
    list_editable = [
        'status',
        'display_order'
    ]
    
    list_per_page = 20
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'author'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'image',
                'designation',
                'description',
                'skills'
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'email',
            )
        }),
        ('Social Media Links', {
            'fields': (
                'facebook',
                'twitter',
                'linkedin',
                'tiktok',
            ),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': (
                'status',
                'display_order',
            )
        }),
        ('Audit Information', {
            'fields': (
                'author',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.image.url
            )
        return "No Image"
    display_image.short_description = 'Image'
    
    def get_skills_list(self, obj):
        return ", ".join(obj.get_skills_list())
    get_skills_list.short_description = 'Skills'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly_fields.append('author')
        return readonly_fields

    class Media:
        css = {
            'all': ('admin/css/teams_admin.css',)
        }