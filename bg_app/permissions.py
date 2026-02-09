from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


def has_permission(user, permission_codename):
    """
    Check if user has specific permission using Django's permission system
    """
    return user.has_perm(permission_codename)


def check_access_permission(user, required_permission=None, role_name=None):
    """
    Unified permission check for views
    """
    if user.is_superuser:
        return True
    
    if required_permission and user.has_perm(required_permission):
        return True
    
    if role_name and user.role == role_name:
        return True
    
    return False


def permission_required(permission_codename, login_url=None):
    """
    Decorator to check for specific permissions
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if check_access_permission(request.user, permission_codename):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect(login_url or 'bg_app:profile')
        return wrapped_view
    return decorator


def role_required(role_name, login_url=None):
    """
    Decorator to check for specific role
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if check_access_permission(request.user, role_name=role_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f"Access restricted to {role_name} role.")
                return redirect(login_url or 'bg_app:profile')
        return wrapped_view
    return decorator


def staff_permission_required(permission_type):
    """
    Decorator specifically for staff permission checks
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('bg_app:login')
            
            if request.user.is_superuser or request.user.is_admin_user():
                return view_func(request, *args, **kwargs)
            
            if not request.user.is_staff_user():
                messages.error(request, "This section is for staff members only.")
                return redirect('bg_app:profile')
            
            # Check staff-specific permissions
            if hasattr(request.user, 'staff_permission_profile'):
                staff_profile = request.user.staff_permission_profile
                
                permission_map = {
                    'manage_students': staff_profile.can_manage_students,
                    'manage_financial': staff_profile.can_manage_financial,
                    'view_reports': staff_profile.can_view_reports,
                    'manage_content': staff_profile.can_manage_content,
                    'manage_courses': staff_profile.can_manage_courses,
                }
                
                if permission_map.get(permission_type, False):
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, "You don't have sufficient staff permissions to access this page.")
            return redirect('bg_app:staff_dashboard')
        return wrapped_view
    return decorator


def multiple_permissions_required(permissions, logical_operator='AND', login_url=None):
    """
    Decorator to check for multiple permissions
    """
    def check_perms(user):
        if user.is_superuser:
            return True
        
        has_perms = [user.has_perm(perm) for perm in permissions]
        
        if logical_operator == 'AND':
            return all(has_perms)
        elif logical_operator == 'OR':
            return any(has_perms)
        return False

    return user_passes_test(check_perms, login_url=login_url)


class PermissionRequiredMixin:
    """
    Class-based view mixin for permission checking
    """
    permission_required = None
    role_required = None
    login_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url or 'bg_app:login')

        if check_access_permission(request.user, self.permission_required, self.role_required):
            return super().dispatch(request, *args, **kwargs)
        
        messages.error(request, "You don't have permission to access this page.")
        return redirect(self.login_url or 'bg_app:profile')


class StaffPermissionRequiredMixin:
    """
    Class-based view mixin for staff permission checking
    """
    staff_permission_required = None
    login_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url or 'bg_app:login')

        if request.user.is_superuser or request.user.is_admin_user():
            return super().dispatch(request, *args, **kwargs)
        
        if not request.user.is_staff_user():
            messages.error(request, "This section is for staff members only.")
            return redirect(self.login_url or 'bg_app:profile')
        
        if self.staff_permission_required and hasattr(request.user, 'staff_permission_profile'):
            staff_profile = request.user.staff_permission_profile
            
            permission_map = {
                'manage_students': staff_profile.can_manage_students,
                'manage_financial': staff_profile.can_manage_financial,
                'view_reports': staff_profile.can_view_reports,
                'manage_content': staff_profile.can_manage_content,
                'manage_courses': staff_profile.can_manage_courses,
            }
            
            if permission_map.get(self.staff_permission_required, False):
                return super().dispatch(request, *args, **kwargs)
        
        messages.error(request, "You don't have sufficient staff permissions to access this page.")
        return redirect(self.login_url or 'bg_app:staff_dashboard')