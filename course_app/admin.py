from django.contrib import admin
from .models import Course, Media, CourseEnrollment

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ['media_type', 'file', 'caption', 'status', 'order']
    ordering = ['order']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_display', 'price', 'offer_price', 'status', 'author', 'created_at']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['title', 'short_description', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MediaInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'image', 'short_description', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('duration', 'price', 'offer_price')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'author', 'created_at', 'updated_at')
        }),
    )
    
    def duration_display(self, obj):
        return obj.duration_display()
    duration_display.short_description = 'Duration'
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['course', 'media_type', 'file_type_icon', 'caption', 'status', 'order', 'created_at']
    list_filter = ['media_type', 'status', 'created_at']
    search_fields = ['course__title', 'caption']
    list_editable = ['status', 'order']
    ordering = ['course', 'order']
    
    def file_type_icon(self, obj):
        return obj.file_type_icon()
    file_type_icon.short_description = 'Type'


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 
        'course', 
        'email', 
        'contact_number', 
        'education_display', 
        'experience_display', 
        'source_display', 
        'enrolled_at', 
        'status'
    ]
    list_filter = [
        'status', 
        'enrolled_at', 
        'education', 
        'experience', 
        'source',
        'course'
    ]
    search_fields = [
        'first_name', 
        'last_name', 
        'email', 
        'contact_number', 
        'course__title',
        'address'
    ]
    readonly_fields = ['enrolled_at']
    list_editable = ['status']
    ordering = ['-enrolled_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': (
                'first_name', 
                'last_name', 
                'email', 
                'contact_number', 
                'address'
            )
        }),
        ('Education & Experience', {
            'fields': (
                'education', 
                'experience'
            )
        }),
        ('Course Information', {
            'fields': (
                'course',
                'source'
            )
        }),
        ('Status & Metadata', {
            'fields': (
                'status', 
                'enrolled_at'
            )
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Student Name'
    full_name.admin_order_field = 'first_name'
    
    def education_display(self, obj):
        return obj.get_education_display() if obj.education else 'Not specified'
    education_display.short_description = 'Education'
    
    def experience_display(self, obj):
        return obj.get_experience_display() if obj.experience else 'Not specified'
    experience_display.short_description = 'Experience'
    
    def source_display(self, obj):
        return obj.get_source_display() if obj.source else 'Not specified'
    source_display.short_description = 'Source'
    
    # Optional: Add actions for bulk operations
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f'{updated} enrollments marked as active.')
    mark_as_active.short_description = "Mark selected enrollments as active"
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, f'{updated} enrollments marked as inactive.')
    mark_as_inactive.short_description = "Mark selected enrollments as inactive"