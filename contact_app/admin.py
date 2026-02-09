from django.contrib import admin
from .models import Branch, Contact


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'address', 'email', 'phone')
    readonly_fields = ('get_phone_numbers',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'image', 'description', 'maps', 'address', 'status')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'office_open')
        }),
        ('Social Links', {
            'fields': ('facebook', 'twitter', 'linkedin', 'instagram')
        }),
    )

    def get_phone_numbers_display(self, obj):
        return ", ".join(obj.get_phone_numbers())
    get_phone_numbers_display.short_description = "Phone Numbers"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'service', 'status', 'is_read', 'created_at')
    list_filter = ('status', 'is_read', 'created_at', 'service')
    search_fields = ('full_name', 'email', 'phone_number', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone_number', 'service')
        }),
        ('Message Details', {
            'fields': ('message', 'status', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} message(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"
