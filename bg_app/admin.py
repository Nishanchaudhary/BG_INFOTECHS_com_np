# bg_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Student, Staff, StaffPermission

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_permissions_count', 'get_users_count', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['permissions']
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permissions Count'
    
    def get_users_count(self, obj):
        return obj.users.count()
    get_users_count.short_description = 'Users Count'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('profile_picture', 'role', 'phone_number', 'address', 'status')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('profile_picture', 'role', 'phone_number', 'address', 'status')
        }),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrollment_number', 'qualification', 'total_fees', 'fees_paid', 'admission_date']
    list_filter = ['qualification', 'admission_date']
    search_fields = ['user__username', 'enrollment_number', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'position', 'salary', 'paid_salary', 'join_date']
    list_filter = ['department', 'position', 'join_date']
    search_fields = ['user__username', 'employee_id', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']

@admin.register(StaffPermission)
class StaffPermissionAdmin(admin.ModelAdmin):
    list_display = ['staff_user', 'is_active', 'get_permissions_count', 'get_groups_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['staff_user__username', 'staff_user__first_name', 'staff_user__last_name']
    filter_horizontal = ['django_permissions', 'groups']
    
    def get_permissions_count(self, obj):
        return obj.django_permissions.count()
    get_permissions_count.short_description = 'Direct Permissions'
    
    def get_groups_count(self, obj):
        return obj.groups.count()
    get_groups_count.short_description = 'Groups Count'