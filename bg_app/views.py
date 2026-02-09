# bg_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.urls import reverse
from django.core.paginator import Paginator
import json
import logging

from .models import User, Student, Staff, Role, StaffPermission
from .forms import UserForm, StudentForm, StaffForm, UserUpdateForm, RoleForm
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

# =============================================================================
# RBAC PERMISSION DECORATORS
# =============================================================================

def rbac_permission_required(permission):
    """
    Custom decorator for RBAC permission checking
    """
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has the specific permission
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            
            # Check role-based access for admin
            if request.user.role and request.user.role.name == 'admin':
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "You don't have permission to access this page.")
            return redirect('bg_app:profile')
        return wrapped_view
    return decorator

def rbac_role_required(role_name):
    """
    Custom decorator for role-based access control
    """
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.role and request.user.role.name == role_name:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f"Access restricted to {role_name} role.")
            return redirect('bg_app:profile')
        return wrapped_view
    return decorator

# =============================================================================
# PERMISSION CHECK FUNCTIONS
# =============================================================================

def has_permission(user, permission_codename):
    """Check if user has specific permission"""
    return user.has_perm(permission_codename)

def check_access(user, permission=None, role=None):
    """Unified permission check"""
    if user.is_superuser:
        return True
    if permission and user.has_perm(permission):
        return True
    if role and user.role and user.role.name == role:
        return True
    return False

# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================

def login_view(request):
    """Handle user authentication and login"""
    if request.user.is_authenticated:
        return redirect_to_dashboard(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                user.login_count += 1
                user.save(update_fields=['login_count', 'last_login'])
                
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                logger.info(f"User {user.username} logged in successfully")
                return redirect_to_dashboard(user)
            else:
                messages.error(request, 'Your account is deactivated. Please contact administrator.')
                logger.warning(f"Deactivated user {username} attempted login")
        else:
            messages.error(request, 'Invalid username or password')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render(request, 'registration/login.html')

def redirect_to_dashboard(user):
    """Redirect users to appropriate dashboard"""
    try:
        if user.is_superuser:
            return redirect('bg_app:admin_dashboard')
        
        if user.role:
            role_name = user.role.name.lower()
            
            if role_name == 'admin' and user.has_perm('bg_app.view_admin_dashboard'):
                return redirect('bg_app:admin_dashboard')
            elif role_name == 'staff' and user.has_perm('bg_app.view_staff_dashboard'):
                return redirect('bg_app:staff_dashboard')
            elif role_name == 'student' and user.has_perm('bg_app.view_student_dashboard'):
                return redirect('bg_app:student_dashboard')
        
        # Fallback based on permissions
        if user.has_perm('bg_app.view_admin_dashboard'):
            return redirect('bg_app:admin_dashboard')
        elif user.has_perm('bg_app.view_staff_dashboard'):
            return redirect('bg_app:staff_dashboard')
        elif user.has_perm('bg_app.view_student_dashboard'):
            return redirect('bg_app:student_dashboard')
        return redirect('bg_app:profile')
        
    except Exception as e:
        logger.error(f"Error redirecting user {user.username}: {str(e)}")
        return redirect('bg_app:profile')

def logout_view(request):
    """Handle user logout"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, 'You have been logged out successfully')
        logger.info(f"User {username} logged out")
    return redirect('bg_app:login')

# =============================================================================
# DASHBOARD VIEWS
# =============================================================================

@login_required
def dashboard_redirect(request):
    """Redirect user to their appropriate dashboard"""
    return redirect_to_dashboard(request.user)

@rbac_permission_required('bg_app.view_admin_dashboard')
def admin_dashboard(request):
    try:
        user = request.user

        student_role_users = User.objects.filter(role__name='student')
        for student_user in student_role_users:
            if not hasattr(student_user, 'student_profile'):
                Student.objects.create(
                    user=student_user,
                    enrollment_number=f"ENR{student_user.id:03d}",
                    qualification="Not specified",
                    training="General Training",
                    total_fees=0,
                    fees_paid=0,
                    admission_date=student_user.date_joined.date()
                )
        
        staff_role_users = User.objects.filter(role__name='staff')
        for staff_user in staff_role_users:
            if not hasattr(staff_user, 'staff_profile'):
                Staff.objects.create(
                    user=staff_user,
                    employee_id=f"EMP{staff_user.id:03d}",
                    department="General",
                    position="Staff",
                    salary=0,
                    paid_salary=0,
                    join_date=staff_user.date_joined.date()
                )
        
        # Get counts after creating profiles
        total_users = User.objects.count()
        admin_users = User.objects.filter(role__name='admin').count()
        staff_users_count = User.objects.filter(role__name='staff').count()
        student_users_count = User.objects.filter(role__name='student').count()
        
        # Get recent data
        recent_users = User.objects.select_related('role').order_by('-date_joined')[:5]
        recent_students = Student.objects.select_related('user').order_by('-admission_date')[:5]
        recent_staff = Staff.objects.select_related('user').order_by('-join_date')[:5]

        context = {
            'user': user,
            'total_users': total_users,
            'active_users': User.objects.filter(is_active=True).count(),
            'inactive_users': User.objects.filter(is_active=False).count(),
            'admin_users': admin_users,
            'staff_users': staff_users_count,
            'student_users': student_users_count,
            'recent_users': recent_users,
            'recent_students': recent_students,
            'recent_staff': recent_staff,
        }
        return render(request, 'admin_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {str(e)}", exc_info=True)
        messages.error(request, 'Error loading dashboard')
        return redirect('bg_app:profile')
    
@rbac_permission_required('bg_app.view_student_dashboard')
def student_dashboard(request):
    """Student dashboard"""
    try:
        user = request.user
        profile = Student.objects.get(user=user)
        
        context = {
            'user': user,
            'profile': profile,
            'fees_paid_percentage': profile.fees_paid_percentage,
            'fees_due': profile.fees_due,
        }
        return render(request, 'student_dashboard.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, 'Please complete your student profile.')
        return redirect('bg_app:profile')
    except Exception as e:
        logger.error(f"Error loading student dashboard: {str(e)}")
        messages.error(request, 'Error loading dashboard')
        return redirect('bg_app:profile')

@rbac_permission_required('bg_app.view_staff_dashboard')
def staff_dashboard(request):
    """Staff dashboard"""
    try:
        user = request.user
        profile = Staff.objects.get(user=user)
        
        context = {
            'user': user,
            'profile': profile,
            'salary_paid_percentage': profile.salary_paid_percentage,
            'salary_due': profile.salary_due,
        }  
        return render(request, 'staff_dashboard.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, 'Please complete your staff profile.')
        return redirect('bg_app:profile')
    except Exception as e:
        logger.error(f"Error loading staff dashboard: {str(e)}")
        messages.error(request, 'Error loading dashboard')
        return redirect('bg_app:profile')

# =============================================================================
# USER MANAGEMENT VIEWS
# =============================================================================

@rbac_permission_required('bg_app.view_user')
def user_list(request):
    """User list page"""
    context = {
        'page_title': 'User Management',
        'breadcrumb_active': 'User List'
    }
    return render(request, 'users/list.html', context)

@rbac_permission_required('bg_app.view_user')
def user_detail(request, pk):
    """User detail page"""
    user = get_object_or_404(User, pk=pk)
    profile = None
    profile_type = None
    
    if hasattr(user, 'student_profile'):
        profile = user.student_profile
        profile_type = 'student'
    elif hasattr(user, 'staff_profile'):
        profile = user.staff_profile
        profile_type = 'staff'
    
    context = {
        'user_obj': user,
        'profile': profile,
        'profile_type': profile_type,
        'page_title': f'User Details - {user.username}',
        'breadcrumb_active': 'User Details'
    }
    return render(request, 'users/detail.html', context)

@rbac_permission_required('bg_app.add_user')
@require_http_methods(["GET", "POST"])
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    
                    messages.success(request, f'User {user.username} created successfully')
                    return redirect('bg_app:user_list')
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                messages.error(request, 'Error creating user')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()
    
    context = {
        'form': form,
        'page_title': 'Create User',
        'breadcrumb_active': 'Create User'
    }
    return render(request, 'users/create.html', context)

@rbac_permission_required('bg_app.change_user')
@require_http_methods(["GET", "POST"])
def user_edit(request, pk):
    """Edit user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'User updated successfully!')
                return redirect('bg_app:user_list')
            except Exception as e:
                logger.error(f"Error updating user {user.username}: {str(e)}")
                messages.error(request, 'Error updating user')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
        'page_title': 'Edit User',
        'breadcrumb_active': 'Edit User'
    }
    return render(request, 'users/edit.html', context)

@rbac_permission_required('bg_app.delete_user')
@require_http_methods(["GET", "POST"])
def user_delete(request, pk):
    """Delete user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        try:
            username = user.username
            user.delete()
            messages.success(request, f'User {username} deleted successfully')
            return redirect('bg_app:user_list')
        except Exception as e:
            logger.error(f"Error deleting user {user.username}: {str(e)}")
            messages.error(request, 'Error deleting user')
            return redirect('bg_app:user_list')
    
    context = {
        'user_obj': user,
        'page_title': 'Delete User',
        'breadcrumb_active': 'Delete User'
    }
    return render(request, 'users/confirm_delete.html', context)

@rbac_permission_required('bg_app.change_user')
@require_http_methods(["POST"])
def user_toggle_status(request, pk):
    """Toggle user active status (AJAX)"""
    try:
        user = get_object_or_404(User, pk=pk)
        
        # Only allow toggling for non-superuser/admin roles
        user_role_name = user.role.name.lower() if user.role else ''
        if any(role in user_role_name for role in ['superuser', 'admin']) or user.is_superuser:
            return JsonResponse({
                'success': False, 
                'error': 'Cannot toggle status for superuser/admin roles'
            }, status=403)
        
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({
            'success': True, 
            'new_status': user.is_active,
            'status_text': 'Active' if user.is_active else 'Inactive'
        })
    except Exception as e:
        logger.error(f"Error toggling user status: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@rbac_permission_required('bg_app.view_user')
def user_datatables_api(request):
    """API endpoint for DataTables user data with role filtering"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Get role filter parameters from frontend
        exclude_roles = request.GET.get('exclude_roles', '').split(',')
        include_roles = request.GET.get('include_roles', '').split(',')
        
        # Base queryset
        users = User.objects.select_related('role').prefetch_related('user_permissions', 'groups')
        
        # Apply role filtering
        # Exclude superuser and admin roles
        if exclude_roles and exclude_roles != ['']:
            if 'superuser' in exclude_roles:
                users = users.exclude(
                    Q(role__name__icontains='superuser') | 
                    Q(is_superuser=True)
                )
            if 'admin' in exclude_roles:
                users = users.exclude(role__name__icontains='admin')
        
        # Include only staff and student roles
        if include_roles and include_roles != ['']:
            role_filter = Q()
            if 'staff' in include_roles:
                role_filter |= Q(role__name__icontains='staff')
            if 'student' in include_roles:
                role_filter |= Q(role__name__icontains='student')
            users = users.filter(role_filter)
        
        # Total records count (after role filtering)
        total_records = users.count()
        
        # Search functionality
        if search_value:
            users = users.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(role__name__icontains=search_value)
            )
        
        # Filtered records count (after search)
        filtered_records = users.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'username',  # Username column
            '1': 'first_name',  # Full name column  
            '2': 'email',  # Email column
            '3': 'role__name',  # Role column
            '4': 'is_active',  # Status column
            '5': 'date_joined'  # Date joined column
        }
        
        order_field = column_map.get(order_column_index, 'username')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        users = users.order_by(order_field)
        
        # Pagination
        users = users[start:start + length]
        
        # Prepare data for response
        data = []
        for user in users:
            # Profile picture
            profile_pic_html = '''
                <div class="profile-image-placeholder">
                    <i class="fas fa-user"></i>
                </div>
            '''
            if user.profile_picture:
                profile_pic_html = f'''
                    <img src="{user.profile_picture.url}" alt="{user.username}" 
                         class="user-thumbnail" 
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="profile-image-placeholder" style="display: none;">
                        <i class="fas fa-user"></i>
                    </div>
                '''
            
            # Full name
            full_name = user.get_full_name() or '<span class="text-muted">Not specified</span>'
            
            # Role badge - Handle role display
            role_name = user.role.name if user.role else 'No Role'
            role_badge_class = "bg-secondary"  # Default
            if role_name.lower() == 'staff':
                role_badge_class = "bg-success"
            elif role_name.lower() == 'student':
                role_badge_class = "bg-info"
            elif role_name.lower() == 'admin':
                role_badge_class = "bg-warning"
            elif 'superuser' in role_name.lower():
                role_badge_class = "bg-danger"
                
            role_html = f'''
                <span class="badge {role_badge_class} rounded-pill">
                    {role_name.title()}
                </span>
            '''
            
            # Status
            status_html = f'''
                <span class="badge bg-{"success" if user.is_active else "danger"} rounded-pill">
                    <i class="fas fa-{"check" if user.is_active else "times"}-circle me-1"></i>
                    {"Active" if user.is_active else "Inactive"}
                </span>
            '''
            
            # Date joined
            date_joined = user.date_joined.strftime('%b %d, %Y') if user.date_joined else 'N/A'
            
            # Actions - Only show for non-superuser roles
            actions_html = ''
            user_role_name = user.role.name.lower() if user.role else ''
            
            # Only show actions for staff and student roles (not superuser/admin)
            if not any(role in user_role_name for role in ['superuser', 'admin']) and not user.is_superuser:
                detail_url = reverse('bg_app:user_detail', args=[user.pk])
                edit_url = reverse('bg_app:user_edit', args=[user.pk])
                delete_url = reverse('bg_app:user_delete', args=[user.pk])
                toggle_url = reverse('bg_app:user_toggle_status', args=[user.pk])
                
                actions_html = f'''
                    <div class="btn-group-vertical btn-group-sm" role="group">
                        <div class="btn-group btn-group-sm" role="group">
                            <a href="{detail_url}" class="btn btn-outline-info" 
                               data-bs-toggle="tooltip" title="View Details">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="{edit_url}" class="btn btn-outline-warning" 
                               data-bs-toggle="tooltip" title="Edit User">
                                <i class="fas fa-edit"></i>
                            </a>
                            <button class="btn btn-outline-{"danger" if user.is_active else "success"} toggle-status" 
                                    data-user-id="{user.pk}" 
                                    data-url="{toggle_url}"
                                    data-bs-toggle="tooltip" 
                                    title="{"Deactivate" if user.is_active else "Activate"} User">
                                <i class="fas fa-{"times" if user.is_active else "check"}"></i>
                            </button>
                            <a href="{delete_url}" class="btn btn-outline-danger" 
                               onclick="return confirm('Are you sure you want to delete this user?')"
                               data-bs-toggle="tooltip" title="Delete User">
                                <i class="fas fa-trash"></i>
                            </a>
                        </div>
                    </div>
                '''
            else:
                # Show message for superuser/admin roles
                actions_html = '''
                    <span class="text-muted small">Restricted</span>
                '''
            
            data.append({
                'profile_picture': profile_pic_html,
                'username': user.username,
                'full_name': full_name,
                'email': user.email,
                'role': role_html,
                'status': status_html,
                'date_joined': date_joined,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        logger.info(f"DataTables API: Returning {len(data)} users (filtered by roles)")
        return JsonResponse(response)
    
    except Exception as e:
        logger.error(f"Error in user_datatables_api: {str(e)}", exc_info=True)
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        }, status=500)



# =============================================================================
# ROLE MANAGEMENT VIEWS
# =============================================================================

@rbac_permission_required('bg_app.manage_roles')
def role_list(request):
    """List all roles with permission counts"""
    try:
        roles = Role.objects.all().prefetch_related('permissions', 'users')
        
        # Add permission counts for each role
        for role in roles:
            role.perms_count = role.permissions.count()
            role.users_count = role.users.count()
        
        context = {
            'roles': roles,
            'page_title': 'Role Management',
            'breadcrumb_active': 'Roles'
        }
        return render(request, 'rbac/role_list.html', context)
    except Exception as e:
        logger.error(f"Error loading role list: {str(e)}")
        messages.error(request, 'Error loading roles')
        return redirect('bg_app:admin_dashboard')

@rbac_permission_required('bg_app.manage_roles')
@require_http_methods(["GET", "POST"])
def role_create(request):
    """Create a new role with permissions"""
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    role = form.save()
                    messages.success(request, f'Role "{role.name}" created successfully with {role.permissions.count()} permissions')
                    logger.info(f"Role {role.name} created by {request.user.username}")
                    return redirect('bg_app:role_list')
            except Exception as e:
                logger.error(f"Error creating role: {str(e)}")
                messages.error(request, f'Error creating role: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = RoleForm()
    
    context = {
        'form': form,
        'title': 'Create Role',
        'page_title': 'Create New Role',
        'breadcrumb_active': 'Create Role'
    }
    return render(request, 'rbac/role_form.html', context)

@rbac_permission_required('bg_app.manage_roles')
@require_http_methods(["GET", "POST"])
def role_edit(request, role_id):
    """Edit an existing role and its permissions"""
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, f'Role "{role.name}" updated successfully')
                    logger.info(f"Role {role.name} updated by {request.user.username}")
                    return redirect('bg_app:role_list')
            except Exception as e:
                logger.error(f"Error updating role {role.name}: {str(e)}")
                messages.error(request, f'Error updating role: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = RoleForm(instance=role)
    
    context = {
        'form': form,
        'title': 'Edit Role',
        'page_title': f'Edit Role - {role.get_name_display()}',
        'breadcrumb_active': 'Edit Role'
    }
    return render(request, 'rbac/role_form.html', context)

@rbac_permission_required('bg_app.manage_roles')
@require_http_methods(["GET", "POST"])
def role_delete(request, role_id):
    """Delete a role"""
    role = get_object_or_404(Role, id=role_id)
    
    # Prevent deletion of system roles
    if role.name in ['admin', 'staff', 'student']:
        messages.error(request, f'System role "{role.get_name_display()}" cannot be deleted.')
        return redirect('bg_app:role_list')
    
    if request.method == 'POST':
        try:
            role_name = role.get_name_display()
            users_count = role.users.count()
            
            # Check if role has users
            if users_count > 0:
                messages.error(request, f'Cannot delete role "{role_name}" because it has {users_count} user(s) assigned. Please reassign users first.')
                return redirect('bg_app:role_list')
            
            role.delete()
            messages.success(request, f'Role "{role_name}" deleted successfully')
            logger.info(f"Role {role_name} deleted by {request.user.username}")
            return redirect('bg_app:role_list')
        except Exception as e:
            logger.error(f"Error deleting role {role.name}: {str(e)}")
            messages.error(request, f'Error deleting role: {str(e)}')
            return redirect('bg_app:role_list')
    
    context = {
        'role': role,
        'page_title': f'Delete Role - {role.get_name_display()}',
        'breadcrumb_active': 'Delete Role'
    }
    return render(request, 'rbac/role_confirm_delete.html', context)

# =============================================================================
# PERMISSION MANAGEMENT VIEWS
# =============================================================================

@rbac_permission_required('bg_app.manage_staff')
def staff_permissions(request):
    """List all staff users and their permissions"""
    try:
        # Get staff role users
        staff_users = User.objects.filter(
            role__name='staff'
        ).select_related('role').prefetch_related(
            'user_permissions', 'groups'
        ).order_by('username')
        
        # Add permission and group information
        for staff in staff_users:
            staff.direct_perms_count = staff.user_permissions.count()
            staff.groups_count = staff.groups.count()
            staff.group_names = list(staff.groups.values_list('name', flat=True))
        
        logger.info(f"Loaded {staff_users.count()} staff users for user {request.user.username}")
        
        context = {
            'staff_users': staff_users,
            'page_title': 'Staff Permissions Management',
            'breadcrumb_active': 'Staff Permissions'
        }
        return render(request, 'rbac/staff_permissions.html', context)
        
    except Exception as e:
        logger.error(f"Error loading staff permissions: {str(e)}", exc_info=True)
        messages.error(request, f'Error loading staff permissions: {str(e)}')
        return redirect('bg_app:admin_dashboard')
    
@rbac_permission_required('bg_app.manage_staff')
def staff_datatables_api(request):
    """API endpoint for DataTable to fetch staff users with pagination and search"""
    try:
        # Get parameters from DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Get ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Base queryset
        staff_users = User.objects.filter(
            role__name='staff'
        ).select_related('role', 'staff_profile').prefetch_related(
            'user_permissions', 'groups'
        )
        
        # Apply search filter
        if search_value:
            staff_users = staff_users.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(staff_profile__department__icontains=search_value) |
                Q(staff_profile__position__icontains=search_value)
            )
        
        # Total records count
        total_records = staff_users.count()
        
        # Apply ordering
        column_mapping = {
            '0': 'username',  # Username
            '1': 'first_name',  # Full name - order by first name
            '2': 'email',  # Email
            '3': 'is_active',  # Status
            '4': 'groups',  # Groups count - custom ordering
            '5': 'user_permissions',  # Permissions count - custom ordering
        }
        
        order_column = column_mapping.get(order_column_index, 'username')
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        
        # Apply custom ordering for counts
        if order_column_index == '4':  # Groups count
            staff_users = staff_users.annotate(groups_count=Count('groups'))
            order_column = 'groups_count' if order_direction == 'asc' else '-groups_count'
        elif order_column_index == '5':  # Permissions count
            staff_users = staff_users.annotate(perms_count=Count('user_permissions'))
            order_column = 'perms_count' if order_direction == 'asc' else '-perms_count'
        
        staff_users = staff_users.order_by(order_column)
        
        # Apply pagination
        paginator = Paginator(staff_users, length)
        page_number = (start // length) + 1
        page_obj = paginator.get_page(page_number)
        
        # Prepare data for response
        data = []
        for staff in page_obj:
            # Username (simple text without profile image)
            username_html = f'<strong>{staff.username}</strong>'
            
            # Full name
            full_name = staff.get_full_name() or '-'
            
            # Email
            email = staff.email or '-'
            
            # Status badge
            if staff.is_active:
                status_html = '<span class="badge bg-success">Active</span>'
            else:
                status_html = '<span class="badge bg-danger">Inactive</span>'
            
            # Groups information
            groups_count = staff.groups.count()
            group_names = list(staff.groups.values_list('name', flat=True))
            if groups_count > 0:
                groups_html = f'''
                    <span class="badge bg-primary" data-bs-toggle="tooltip" 
                          title="{', '.join(group_names)}">
                        {groups_count} group(s)
                    </span>
                '''
            else:
                groups_html = '<span class="text-muted">No groups</span>'
            
            # Direct permissions count
            perms_count = staff.user_permissions.count()
            if perms_count > 0:
                perms_html = f'<span class="badge bg-info">{perms_count} permission(s)</span>'
            else:
                perms_html = '<span class="text-muted">No direct permissions</span>'
            
            # Actions
            actions_html = f'''
                <div class="btn-group btn-group-sm">
                    <a href="{reverse('bg_app:edit_staff_permissions', args=[staff.id])}" 
                       class="btn btn-primary" data-bs-toggle="tooltip" title="Edit Permissions">
                        <i class="fas fa-edit"></i>
                    </a>
                    <button class="btn btn-{'warning' if staff.is_active else 'success'} toggle-status" 
                            data-user-id="{staff.id}" 
                            data-url="{reverse('bg_app:toggle_staff_status', args=[staff.id])}"
                            data-bs-toggle="tooltip" 
                            title="{'Deactivate' if staff.is_active else 'Activate'}">
                        <i class="fas fa-{'times' if staff.is_active else 'check'}"></i>
                    </button>
                </div>
            '''
            
            data.append({
                'username': username_html,
                'full_name': full_name,
                'email': email,
                'status': status_html,
                'groups': groups_html,
                'permissions': perms_html,
                'actions': actions_html,
                'DT_RowId': f'staff_{staff.id}'
            })
        
        response_data = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in staff datatables API: {str(e)}", exc_info=True)
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        }, status=500)


@rbac_permission_required('bg_app.manage_staff')
@require_http_methods(["GET", "POST"])
def edit_staff_permissions(request, user_id):
    """Edit permissions for a staff user"""
    try:
        # Get staff user
        staff_user = get_object_or_404(User, id=user_id, role__name='staff')
        
        # Get all permissions organized by app
        content_types = ContentType.objects.all().order_by('app_label', 'model')
        permissions_by_app = {}
        
        for content_type in content_types:
            app_label = content_type.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {}
            
            model_permissions = Permission.objects.filter(
                content_type=content_type
            ).order_by('codename')
            
            if model_permissions.exists():
                permissions_by_app[app_label][content_type.model] = {
                    'content_type': content_type,
                    'permissions': model_permissions
                }
        
        # Get all groups
        all_groups = Group.objects.all().order_by('name')
        
        # Get user's current permissions and groups
        user_permissions = set(staff_user.user_permissions.values_list('id', flat=True))
        user_groups = set(staff_user.groups.values_list('id', flat=True))
        
        if request.method == "POST":
            try:
                with transaction.atomic():
                    # Handle individual permissions
                    selected_permission_ids = []
                    for key, value in request.POST.items():
                        if key.startswith('perm_'):
                            try:
                                permission_id = int(key.replace('perm_', ''))
                                selected_permission_ids.append(permission_id)
                            except ValueError:
                                continue
                    
                    # Handle group assignments
                    selected_group_ids = []
                    for key, value in request.POST.items():
                        if key.startswith('group_'):
                            try:
                                group_id = int(key.replace('group_', ''))
                                selected_group_ids.append(group_id)
                            except ValueError:
                                continue
                    
                    # Update user permissions
                    staff_user.user_permissions.set(selected_permission_ids)
                    
                    # Update user groups
                    staff_user.groups.set(selected_group_ids)
                    
                    # Handle user active status
                    is_active = 'is_active' in request.POST
                    if staff_user.is_active != is_active:
                        staff_user.is_active = is_active
                        staff_user.save(update_fields=['is_active'])
                    
                    messages.success(request, f"Permissions updated successfully for {staff_user.get_full_name() or staff_user.username}!")
                    logger.info(f"Permissions updated for staff user {staff_user.username} by {request.user.username}")
                    return redirect('bg_app:staff_permissions')
                    
            except Exception as e:
                logger.error(f"Error updating staff permissions for user {staff_user.username}: {str(e)}", exc_info=True)
                messages.error(request, f"Error updating permissions: {str(e)}")
        
        context = {
            'staff_user': staff_user,
            'permissions_by_app': permissions_by_app,
            'all_groups': all_groups,
            'user_permissions': user_permissions,
            'user_groups': user_groups,
            'page_title': f'Edit Permissions - {staff_user.get_full_name() or staff_user.username}',
            'breadcrumb_active': 'Edit Permissions'
        }
        
        return render(request, 'rbac/edit_staff_permissions.html', context)
        
    except Exception as e:
        logger.error(f"Error in edit_staff_permissions: {str(e)}", exc_info=True)
        messages.error(request, f"Error loading permissions editor: {str(e)}")
        return redirect('bg_app:staff_permissions')




@rbac_permission_required('bg_app.manage_staff')
@require_http_methods(["POST"])
def toggle_staff_status(request, user_id):
    """Toggle staff user active status (AJAX endpoint)"""
    try:
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'This endpoint only accepts AJAX requests.'}, status=400)
        
        staff_user = get_object_or_404(User, id=user_id, role__name='staff')
        staff_user.is_active = not staff_user.is_active
        staff_user.save(update_fields=['is_active'])
        
        logger.info(f"Staff user {staff_user.username} status toggled to {staff_user.is_active} by {request.user.username}")
        
        return JsonResponse({
            'success': True, 
            'new_status': staff_user.is_active,
            'status_text': 'Active' if staff_user.is_active else 'Inactive',
            'user_name': staff_user.get_full_name() or staff_user.username
        })
        
    except User.DoesNotExist:
        logger.error(f"Staff user not found for status toggle: {user_id}")
        return JsonResponse({'success': False, 'error': 'Staff user not found'}, status=404)
    except Exception as e:
        logger.error(f"Error toggling staff status: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@rbac_permission_required('bg_app.change_user')
def user_permissions(request, user_id):
    """Manage permissions for any user"""
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Get all permissions organized by app
        content_types = ContentType.objects.all().order_by('app_label', 'model')
        permissions_by_app = {}
        
        for content_type in content_types:
            app_label = content_type.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {}
            
            model_permissions = Permission.objects.filter(
                content_type=content_type
            ).order_by('codename')
            
            if model_permissions.exists():
                permissions_by_app[app_label][content_type.model] = {
                    'content_type': content_type,
                    'permissions': model_permissions
                }
        
        # Get all groups
        all_groups = Group.objects.all().order_by('name')
        
        # Get user's current permissions and groups
        user_permissions = set(user.user_permissions.values_list('id', flat=True))
        user_groups = set(user.groups.values_list('id', flat=True))
        
        if request.method == "POST":
            try:
                with transaction.atomic():
                    # Get selected permissions from form
                    selected_permission_ids = []
                    for key in request.POST.keys():
                        if key.startswith('permission_'):
                            permission_id = key.replace('permission_', '')
                            try:
                                selected_permission_ids.append(int(permission_id))
                            except ValueError:
                                continue
                    
                    # Get selected groups from form
                    selected_group_ids = []
                    for key in request.POST.keys():
                        if key.startswith('group_'):
                            group_id = key.replace('group_', '')
                            try:
                                selected_group_ids.append(int(group_id))
                            except ValueError:
                                continue
                    
                    # Update user permissions
                    user.user_permissions.set(selected_permission_ids)
                    
                    # Update user groups
                    user.groups.set(selected_group_ids)
                    
                    messages.success(request, f"Permissions updated successfully for {user.get_full_name() or user.username}!")
                    logger.info(f"Permissions updated for user {user.username} by {request.user.username}")
                    return redirect('bg_app:user_detail', pk=user_id)
                    
            except Exception as e:
                logger.error(f"Error updating user permissions for {user.username}: {str(e)}", exc_info=True)
                messages.error(request, f"Error updating permissions: {str(e)}")
        
        context = {
            'user_obj': user,
            'permissions_by_app': permissions_by_app,
            'all_groups': all_groups,
            'user_permissions': user_permissions,
            'user_groups': user_groups,
            'page_title': f'Manage Permissions - {user.get_full_name() or user.username}',
            'breadcrumb_active': 'Manage Permissions'
        }
        
        return render(request, 'rbac/user_permissions.html', context)
        
    except Exception as e:
        logger.error(f"Error in user_permissions: {str(e)}", exc_info=True)
        messages.error(request, f"Error loading user permissions: {str(e)}")
        return redirect('bg_app:user_list')

@rbac_permission_required('bg_app.view_user')
def permission_summary(request, user_id):
    """Display detailed permission summary for a user"""
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Get all permissions (direct + group permissions)
        direct_permissions = user.user_permissions.all().select_related('content_type')
        group_permissions = Permission.objects.filter(group__user=user).select_related('content_type').distinct()
        
        # Combine and deduplicate permissions using set to avoid union issues
        all_permissions_set = set(direct_permissions) | set(group_permissions)
        all_permissions = list(all_permissions_set)
        
        # Organize by app label and model - FIXED STRUCTURE
        permissions_by_app = {}
        for perm in all_permissions:
            app_label = perm.content_type.app_label
            model_name = perm.content_type.model
            
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {}
            
            if model_name not in permissions_by_app[app_label]:
                permissions_by_app[app_label][model_name] = []
            
            permissions_by_app[app_label][model_name].append(perm)
        
        # Get user groups properly
        user_groups = user.groups.all()
        
        context = {
            'user_obj': user,
            'direct_permissions': direct_permissions,
            'group_permissions': group_permissions,
            'all_permissions': all_permissions,
            'permissions_by_app': permissions_by_app,
            'user_groups': user_groups,
            'page_title': f'Permission Summary - {user.get_full_name() or user.username}',
            'breadcrumb_active': 'Permission Summary'
        }
        
        return render(request, 'rbac/permission_summary.html', context)
        
    except Exception as e:
        logger.error(f"Error loading permission summary: {str(e)}", exc_info=True)
        messages.error(request, f'Error loading permission summary: {str(e)}')
        return redirect('bg_app:user_list')

# =============================================================================
# PROFILE MANAGEMENT VIEWS
# =============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    """User profile page"""
    user = request.user
    
    try:
        if hasattr(user, 'student_profile'):
            profile_obj = user.student_profile
            
            class StudentProfileForm(StudentForm):
                class Meta(StudentForm.Meta):
                    exclude = ['total_fees', 'fees_paid']
            
            if request.method == 'POST':
                form = StudentProfileForm(request.POST, instance=profile_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully')
                    return redirect('bg_app:profile')
            else:
                form = StudentProfileForm(instance=profile_obj)
                
            context = {'user': user, 'profile': profile_obj, 'profile_form': form}
                
        elif hasattr(user, 'staff_profile'):
            profile_obj = user.staff_profile
            
            class StaffProfileForm(StaffForm):
                class Meta(StaffForm.Meta):
                    exclude = ['salary', 'paid_salary']
            
            if request.method == 'POST':
                form = StaffProfileForm(request.POST, instance=profile_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully')
                    return redirect('bg_app:profile')
            else:
                form = StaffProfileForm(instance=profile_obj)
                
            context = {'user': user, 'profile': profile_obj, 'profile_form': form}
        else:
            context = {'user': user}
                
    except ObjectDoesNotExist:
        context = {'user': user}
    
    return render(request, 'profile.html', context)

@rbac_permission_required('bg_app.add_user')
@require_http_methods(["GET", "POST"])
def create_student(request, user_id):
    """Create student profile"""
    user = get_object_or_404(User, id=user_id)
    
    if hasattr(user, 'student_profile'):
        messages.warning(request, 'Student profile already exists for this user.')
        return redirect('bg_app:user_detail', pk=user_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save(commit=False)
                student.user = user
                
                if student.fees_paid > student.total_fees:
                    messages.error(request, 'Fees paid cannot exceed total fees')
                    return render(request, 'users/create_profile.html', {'form': form, 'user': user, 'role': 'student'})
                
                student.save()
                messages.success(request, f'Student profile for {user.username} created successfully')
                logger.info(f"Student profile created for {user.username} by {request.user.username}")
                return redirect('bg_app:user_list')
            except Exception as e:
                logger.error(f"Error creating student profile: {str(e)}")
                messages.error(request, 'Error creating student profile')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = StudentForm()
    
    return render(request, 'users/create_profile.html', {'form': form, 'user': user, 'role': 'student'})

@rbac_permission_required('bg_app.add_user')
@require_http_methods(["GET", "POST"])
def create_staff(request, user_id):
    """Create staff profile"""
    user = get_object_or_404(User, id=user_id)
    
    if hasattr(user, 'staff_profile'):
        messages.warning(request, 'Staff profile already exists for this user.')
        return redirect('bg_app:user_detail', pk=user_id)
    
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            try:
                staff = form.save(commit=False)
                staff.user = user
                
                if staff.paid_salary > staff.salary:
                    messages.error(request, 'Paid salary cannot exceed total salary')
                    return render(request, 'users/create_profile.html', {'form': form, 'user': user, 'role': 'staff'})
                
                staff.save()
                messages.success(request, f'Staff profile for {user.username} created successfully')
                logger.info(f"Staff profile created for {user.username} by {request.user.username}")
                return redirect('bg_app:user_list')
            except Exception as e:
                logger.error(f"Error creating staff profile: {str(e)}")
                messages.error(request, 'Error creating staff profile')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = StaffForm()
    
    return render(request, 'users/create_profile.html', {'form': form, 'user': user, 'role': 'staff'})

@rbac_permission_required('bg_app.change_user')
@require_http_methods(["GET", "POST"])
def edit_student(request, user_id):
    """Edit student profile"""
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Student profile for {user.username} updated successfully')
                logger.info(f"Student profile updated for {user.username} by {request.user.username}")
                return redirect('bg_app:user_detail', pk=user.id)
            except Exception as e:
                logger.error(f"Error updating student profile: {str(e)}")
                messages.error(request, 'Error updating student profile')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user, 'role': 'student'})

@rbac_permission_required('bg_app.change_user')
@require_http_methods(["GET", "POST"])
def edit_staff(request, user_id):
    """Edit staff profile"""
    user = get_object_or_404(User, id=user_id)
    staff = get_object_or_404(Staff, user=user)
    
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Staff profile for {user.username} updated successfully')
                logger.info(f"Staff profile updated for {user.username} by {request.user.username}")
                return redirect('bg_app:user_detail', pk=user.id)
            except Exception as e:
                logger.error(f"Error updating staff profile: {str(e)}")
                messages.error(request, 'Error updating staff profile')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = StaffForm(instance=staff)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user, 'role': 'staff'})

@rbac_permission_required('bg_app.manage_financial')
@require_http_methods(["POST"])
def update_student_fees(request, user_id):
    """Update student fees"""
    user = get_object_or_404(User, id=user_id)
    student = get_object_or_404(Student, user=user)
    
    try:
        total_fees = request.POST.get('total_fees')
        fees_paid = request.POST.get('fees_paid')
        
        if total_fees:
            student.total_fees = float(total_fees)
        if fees_paid:
            student.fees_paid = float(fees_paid)
            
        if student.fees_paid > student.total_fees:
            messages.error(request, 'Fees paid cannot exceed total fees')
            return redirect('bg_app:user_detail', user_id=user.id)
            
        student.save()
        messages.success(request, f'Fees updated for {user.username}')
        logger.info(f"Student fees updated for {user.username} by {request.user.username}")
        return redirect('bg_app:user_detail', user_id=user.id)
    except Exception as e:
        logger.error(f"Error updating student fees: {str(e)}")
        messages.error(request, 'Error updating fees')
        return redirect('bg_app:user_detail', user_id=user.id)

@rbac_permission_required('bg_app.manage_financial')
@require_http_methods(["POST"])
def update_staff_salary(request, user_id):
    """Update staff salary"""
    user = get_object_or_404(User, id=user_id)
    staff = get_object_or_404(Staff, user=user)
    
    try:
        salary = request.POST.get('salary')
        paid_salary = request.POST.get('paid_salary')
        
        if salary:
            staff.salary = float(salary)
        if paid_salary:
            staff.paid_salary = float(paid_salary)
            
        if staff.paid_salary > staff.salary:
            messages.error(request, 'Paid salary cannot exceed total salary')
            return redirect('bg_app:user_detail', user_id=user.id)
            
        staff.save()
        messages.success(request, f'Salary updated for {user.username}')
        logger.info(f"Staff salary updated for {user.username} by {request.user.username}")
        return redirect('bg_app:user_detail', user_id=user.id)
    except Exception as e:
        logger.error(f"Error updating staff salary: {str(e)}")
        messages.error(request, 'Error updating salary')
        return redirect('bg_app:user_detail', user_id=user.id)

# =============================================================================
# DJANGO PERMISSION MANAGEMENT VIEWS
# =============================================================================

@rbac_permission_required('auth.change_user')
def custom_admin_dashboard(request, user_id=None):
    """Custom admin dashboard for permission management"""
    try:
        # Get all groups
        all_groups = Group.objects.all().order_by('name')
        
        # Get all permissions grouped by content type
        content_types = ContentType.objects.all()
        permissions_by_app = {}
        
        for ct in content_types:
            app_label = ct.app_label
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {}
            
            model_name = ct.model
            permissions = Permission.objects.filter(content_type=ct)
            
            if permissions.exists():
                permissions_by_app[app_label][model_name] = permissions
        
        # Get user if user_id is provided
        user = None
        user_permissions = set()
        user_groups = set()
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_permissions = set(user.user_permissions.all())
                user_groups = set(user.groups.all())
            except User.DoesNotExist:
                messages.error(request, 'User not found')
        
        context = {
            'permissions_by_app': permissions_by_app,
            'all_groups': all_groups,
            'user': user,
            'user_permissions': user_permissions,
            'user_groups': user_groups,
        }
        
        return render(request, 'admin/custom_admin_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error loading custom admin dashboard: {str(e)}")
        messages.error(request, 'Error loading admin dashboard')
        return redirect('bg_app:admin_dashboard')

@csrf_exempt
@rbac_permission_required('auth.change_user')
@require_http_methods(["POST"])
def save_user_permissions(request, user_id):
    """Save user permissions (AJAX endpoint)"""
    try:
        user = User.objects.get(id=user_id)
        
        # Parse JSON data
        data = json.loads(request.body)
        permission_ids = [int(pid) for pid in data.get('permissions', [])]
        
        # Update user permissions
        user.user_permissions.set(permission_ids)
        
        logger.info(f"Permissions saved for user {user.username} by {request.user.username}")
        
        return JsonResponse({
            'success': True, 
            'message': 'Permissions saved successfully',
            'permissions_count': len(permission_ids)
        })
            
    except User.DoesNotExist:
        logger.error(f"User not found for permission update: {user_id}")
        return JsonResponse({
            'success': False, 
            'error': 'User not found'
        }, status=404)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in save_user_permissions: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': f'Invalid JSON: {str(e)}'
        }, status=400)
    except Exception as e:
        logger.error(f"Error saving permissions: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)

@csrf_exempt
@rbac_permission_required('auth.change_user')
@require_http_methods(["POST"])
def save_user_groups(request, user_id):
    """Save user groups (AJAX endpoint)"""
    try:
        user = User.objects.get(id=user_id)
        data = json.loads(request.body)
        group_ids = [int(gid) for gid in data.get('groups', [])]
        
        # Update user groups
        user.groups.set(group_ids)
        
        logger.info(f"Groups saved for user {user.username} by {request.user.username}")
        
        return JsonResponse({
            'success': True, 
            'message': 'Groups saved successfully'
        })
    except User.DoesNotExist:
        logger.error(f"User not found for group update: {user_id}")
        return JsonResponse({
            'success': False, 
            'error': 'User not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error saving groups: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)