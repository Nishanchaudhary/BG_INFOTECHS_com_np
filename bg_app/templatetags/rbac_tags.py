from django import template

register = template.Library()

@register.filter
def has_permission(user, permission_codename):
    """
    Check if user has specific permission
    Usage: {% if user|has_permission:"app_name.permission_codename" %}
    """
    if not user or not user.is_authenticated:
        return False
    return user.has_perm(permission_codename)

@register.filter
def has_role(user, role_name):
    """
    Check if user has specific role
    Usage: {% if user|has_role:"admin" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    if hasattr(user, 'role') and user.role and user.role.name == role_name:
        return True
    
    return False

@register.filter
def can_view(user, model_name):
    """
    Check if user can view a specific model
    Usage: {% if user|can_view:"features" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    # Handle both "app.model" and just "model" formats
    if '.' in model_name:
        app_label, model = model_name.split('.')
        permission = f"{app_label}.view_{model}"
    else:
        permission = f"company_app.view_{model_name}"
    
    return user.has_perm(permission)

@register.filter
def can_add(user, model_name):
    """
    Check if user can add a specific model
    Usage: {% if user|can_add:"features" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if '.' in model_name:
        app_label, model = model_name.split('.')
        permission = f"{app_label}.add_{model}"
    else:
        permission = f"company_app.add_{model_name}"
    
    return user.has_perm(permission)

@register.filter
def can_change(user, model_name):
    """
    Check if user can change a specific model
    Usage: {% if user|can_change:"features" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if '.' in model_name:
        app_label, model = model_name.split('.')
        permission = f"{app_label}.change_{model}"
    else:
        permission = f"company_app.change_{model_name}"
    
    return user.has_perm(permission)

@register.filter
def can_delete(user, model_name):
    """
    Check if user can delete a specific model
    Usage: {% if user|can_delete:"features" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if '.' in model_name:
        app_label, model = model_name.split('.')
        permission = f"{app_label}.delete_{model}"
    else:
        permission = f"company_app.delete_{model_name}"
    
    return user.has_perm(permission)

@register.simple_tag
def get_user_permissions(user):
    """
    Get all permissions for a user
    Usage: {% get_user_permissions user as user_permissions %}
    """
    if not user or not user.is_authenticated:
        return []
    return user.get_all_permissions()

@register.simple_tag
def check_access(user, permission=None, role=None):
    """
    Unified permission check
    Usage: {% check_access user permission="app.permission" role="admin" as has_access %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    if permission and user.has_perm(permission):
        return True
    
    if role and hasattr(user, 'role') and user.role and user.role.name == role:
        return True
    
    return False

# Simple tag without assignment
@register.simple_tag
def has_access(user, permission, role=None):
    """
    Simple permission check without assignment
    Usage: {% has_access user "app.permission" "admin" %}
    """
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    if user.has_perm(permission):
        return True
    
    if role and hasattr(user, 'role') and user.role and user.role.name == role:
        return True
    
    return False