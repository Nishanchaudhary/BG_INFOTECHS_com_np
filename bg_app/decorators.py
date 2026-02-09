from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

# =============================================================================
# RBAC PERMISSION DECORATORS
# =============================================================================

def rbac_permission_required(permission):
    """
    Custom decorator for RBAC permission checking
    FIXED: Staff users now require explicit permissions
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Allow superusers (bypass all checks)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Staff users require explicit permissions
            if request.user.is_staff:
                if request.user.has_perm(permission):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, "You don't have permission to access this page.")
                    return redirect('bg_app:profile')
            
            # Regular users: Check if user has the specific permission
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            
            # Check role-based access for admin role
            if hasattr(request.user, 'role') and request.user.role and request.user.role.name == 'admin':
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "You don't have permission to access this page.")
            return redirect('bg_app:profile')
        return wrapped_view
    return decorator

def rbac_role_required(role_name):
    """
    Custom decorator for role-based access control
    FIXED: Staff users don't automatically get role access
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Allow superusers only (staff need explicit role)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check role-based access
            if hasattr(request.user, 'role') and request.user.role and request.user.role.name == role_name:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f"Access restricted to {role_name} role.")
            return redirect('bg_app:profile')
        return wrapped_view
    return decorator

# Aliases for backward compatibility
def role_required(role_name):
    return rbac_role_required(role_name)

def permission_required_custom(permission):
    return rbac_permission_required(permission)

# Permission check functions
def has_permission(user, permission_codename):
    """Check if user has specific permission"""
    if user.is_superuser:
        return True
    if user.is_staff:
        return user.has_perm(permission_codename)
    return user.has_perm(permission_codename)

def check_access(user, permission=None, role=None):
    """Unified permission check"""
    if user.is_superuser:
        return True
    if permission and user.has_perm(permission):
        return True
    if role and hasattr(user, 'role') and user.role and user.role.name == role:
        return True
    return False