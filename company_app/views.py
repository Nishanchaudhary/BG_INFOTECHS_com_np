from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.urls import reverse
from bg_app.views import rbac_permission_required
from django.core.exceptions import PermissionDenied
from .models import Company_profile, Features, Services, Testimonials, Project_done,Services_testimonial,Services_faq,Category,Services_success
from .forms import FeaturesForm, ServiceForm, TestimonialForm, ProjectDoneForm,ServicesTestimonialForm,ServicesFaqForm,CategoryForm,ServiceSuccessForm

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def has_company_permission(user, permission_codename):
    """
    Check if user has specific company permission
    """
    return user.is_superuser or (user.role and user.role.name == 'admin') or user.has_perm(permission_codename)

# =============================================================================
# COMPANY PROFILE VIEWS
# =============================================================================

@rbac_permission_required('company_app.manage_company_profile')
def company_profile_view(request):
    """
    Company profile management - accessible to admin and staff with permission
    """
    profile, created = Company_profile.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        # Update company profile fields
        profile.company_name = request.POST.get('company_name')
        profile.company_email = request.POST.get('company_email')
        profile.company_phone = request.POST.get('company_phone')
        profile.company_address = request.POST.get('company_address')
        profile.company_intro = request.POST.get('company_intro')
        profile.company_mission = request.POST.get('company_mission')
        profile.company_vision = request.POST.get('company_vision')
        profile.company_footer = request.POST.get('company_footer')
        profile.map_iframe = request.POST.get('map_iframe')
        profile.facebook_link = request.POST.get('facebook_link')
        profile.instagram_link = request.POST.get('instagram_link')
        profile.twitter_link = request.POST.get('twitter_link')
        profile.youtube_link = request.POST.get('youtube_link')
        profile.meta_title = request.POST.get('meta_title')
        profile.meta_description = request.POST.get('meta_description')
        profile.meta_keywords = request.POST.get('meta_keywords')
        
        # Handle file uploads
        if 'company_logo' in request.FILES:
            profile.company_logo = request.FILES['company_logo']
        if 'company_footer_logo' in request.FILES:
            profile.company_footer_logo = request.FILES['company_footer_logo']
        if 'company_favicon' in request.FILES:
            profile.company_favicon = request.FILES['company_favicon']
        if 'company_image' in request.FILES:
            profile.company_image = request.FILES['company_image']
        
        profile.save()
        messages.success(request, 'Company profile updated successfully!')
        return redirect('company_app:company_profile')
    
    context = {
        'profile': profile,
        'page_title': 'Company Profile',
        'breadcrumb_active': 'Company Profile'
    }
    return render(request, 'company/company_profile.html', context)

# =============================================================================
# FEATURE VIEWS
# =============================================================================

@rbac_permission_required('company_app.view_features')
def feature_list(request):
    """
    Feature list - accessible to users with view_features permission
    """
    context = {
        'page_title': 'Features List',
        'breadcrumb_active': 'Features List'
    }
    return render(request, 'company/feature_list.html', context)

@rbac_permission_required('company_app.view_features')
def features_datatables_api(request):
    """
    Datatables API for features
    """
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            features = Features.objects.all()
        else:
            features = Features.objects.filter(status=True)
        
        # Total records count
        total_records = features.count()
        
        # Search functionality
        if search_value:
            features = features.filter(
                Q(title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(tags__icontains=search_value) |
                Q(icon__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = features.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'description', 
            '2': 'tags',
            '3': 'icon',
            '4': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'title')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        features = features.order_by(order_field)
        
        # Pagination
        features = features[start:start + length]
        
        # Prepare data for response
        data = []
        for feature in features:
            # Render description with truncation
            plain_text = strip_tags(feature.description)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            description_html = f'<span class="description-text" data-bs-toggle="tooltip" title="{plain_text}">{truncated}</span>'
            
            # Render tags as badges
            tags_list = feature.get_tags_list()
            tags_html = '<span class="text-muted">No tags</span>'
            if tags_list:
                badges = []
                colors = ['primary', 'success', 'info', 'warning', 'danger']
                for i, tag in enumerate(tags_list[:3]):
                    color = colors[i % len(colors)]
                    badges.append(f'<span class="badge bg-{color}">{tag}</span>')
                if len(tags_list) > 3:
                    badges.append(f'<span class="badge bg-secondary">+{len(tags_list)-3}</span>')
                tags_html = ' '.join(badges)
            
            # Render icon
            icon_html = f'<i class="{feature.icon} fa-lg text-primary"></i> <span class="ms-2">{feature.icon}</span>' if feature.icon else "-"
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if feature.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render actions - with permission checks
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_company_permission(request.user, 'company_app.change_features')
            can_delete = has_company_permission(request.user, 'company_app.delete_features')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('company_app:feature_edit', args=[feature.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Feature">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:feature_delete', args=[feature.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this feature?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Feature">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'title': feature.title,
                'description': description_html,
                'tags': tags_html,
                'icon': icon_html,
                'status': status_html,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in features_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('company_app.add_features')
def feature_create(request):
    """
    Create new feature - accessible to users with add_features permission
    """
    if request.method == 'POST':
        form = FeaturesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature created successfully!')
            return redirect('company_app:feature_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeaturesForm()
    
    context = {
        'form': form,
        'page_title': 'Create Feature',
        'breadcrumb_active': 'Create Feature',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/feature_form.html', context)

@rbac_permission_required('company_app.change_features')
def feature_edit(request, pk):
    """
    Edit feature - accessible to users with change_features permission
    """
    feature = get_object_or_404(Features, pk=pk)
    
    if request.method == 'POST':
        form = FeaturesForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature updated successfully!')
            return redirect('company_app:feature_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeaturesForm(instance=feature)
    
    context = {
        'form': form,
        'feature': feature,
        'page_title': f'Edit Feature - {feature.title}',
        'breadcrumb_active': 'Edit Feature',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/feature_form.html', context)

@rbac_permission_required('company_app.delete_features')
def feature_delete(request, pk):
    """
    Delete feature - accessible to users with delete_features permission
    """
    feature = get_object_or_404(Features, pk=pk)
    
    if request.method == 'POST':
        feature_name = feature.title
        feature.delete()
        messages.success(request, f'Feature "{feature_name}" deleted successfully!')
        return redirect('company_app:feature_list')
    
    context = {
        'feature': feature,
        'page_title': 'Delete Feature',
        'breadcrumb_active': 'Delete Feature'
    }
    return render(request, 'company/feature_confirm_delete.html', context)

# =============================================================================
# SERVICE VIEWS
# =============================================================================

@rbac_permission_required('company_app.view_services')
def service_list(request):
    """
    Service list - accessible to users with view_services permission
    """
    context = {
        'page_title': 'Services List',
        'breadcrumb_active': 'Services List'
    }
    return render(request, 'company/service_list.html', context)

@rbac_permission_required('company_app.view_services')
def services_datatables_api(request):
    """
    Datatables API for services
    """
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            services = Services.objects.all()
        else:
            services = Services.objects.filter(status=True)
        
        # Total records count
        total_records = services.count()
        
        # Search functionality
        if search_value:
            services = services.filter(
                Q(title__icontains=search_value) |
                Q(sub_title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(icon__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = services.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'sub_title', 
            '2': 'description',
            '3': 'icon',
            '4': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'title')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        services = services.order_by(order_field)
        
        # Pagination
        services = services[start:start + length]
        
        # Prepare data for response
        data = []
        for service in services:
            # Render description with truncation
            plain_text = strip_tags(service.description)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            description_html = f'<span class="description-text" data-bs-toggle="tooltip" title="{plain_text}">{truncated}</span>'
            
            # Render image thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if service.image:
                try:
                    image_html = f'<img src="{service.image.url}" alt="{service.title}" class="img-thumbnail" style="width: 50px; height: 50px; object-fit: cover;">'
                except:
                    image_html = '<span class="text-muted">Image error</span>'
            
            # Render icon
            icon_html = f'<i class="{service.icon} fa-lg text-primary"></i> <span class="ms-2">{service.icon}</span>' if service.icon else '<span class="text-muted">No icon</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if service.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render sub_title with fallback
            sub_title_html = service.sub_title if service.sub_title else '<span class="text-muted">No subtitle</span>'
            
            # Render actions - with permission checks
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has view, edit, or delete permissions
            can_view = has_company_permission(request.user, 'company_app.view_services')
            can_edit = has_company_permission(request.user, 'company_app.change_services')
            can_delete = has_company_permission(request.user, 'company_app.delete_services')
            
            if can_view or can_edit or can_delete:
                actions_buttons = []
                
                if can_view:
                    details_url = reverse('company_app:service_details', args=[service.pk])
                    actions_buttons.append(
                        f'<a href="{details_url}" class="btn btn-outline-info btn-sm" '
                        f'data-bs-toggle="tooltip" title="View Details">'
                        f'<i class="fas fa-eye"></i></a>'
                    )
                
                if can_edit:
                    edit_url = reverse('company_app:service_edit', args=[service.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Service">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:service_delete', args=[service.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this service?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Service">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'title': service.title,
                'sub_title': sub_title_html,
                'description': description_html,
                'image': image_html,
                'icon': icon_html,
                'status': status_html,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in services_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('company_app.view_services')
def service_details(request, pk):
    """View service details"""
    service = get_object_or_404(Services, pk=pk)
    
    context = {
        'service': service,
        'page_title': f'Service Details - {service.title}',
        'breadcrumb_active': 'Service Details'
    }
    return render(request, 'company/service_details.html', context)

@rbac_permission_required('company_app.add_services')
def services_create(request):
    """Create new service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('company_app:service_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'page_title': 'Create Service',
        'breadcrumb_active': 'Create Service',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/service_form.html', context)

@rbac_permission_required('company_app.change_services')
def service_edit(request, pk):
    """Edit existing service"""
    service = get_object_or_404(Services, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('company_app:service_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'service': service,
        'page_title': f'Edit Service - {service.title}',
        'breadcrumb_active': 'Edit Service',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/service_form.html', context)

@rbac_permission_required('company_app.delete_services')
def service_delete(request, pk):
    """Delete service"""
    service = get_object_or_404(Services, pk=pk)
    
    if request.method == 'POST':
        service_name = service.title
        service.delete()
        messages.success(request, f'Service "{service_name}" deleted successfully!')
        return redirect('company_app:service_list')
    
    context = {
        'service': service,
        'page_title': 'Delete Service',
        'breadcrumb_active': 'Delete Service'
    }
    return render(request, 'company/service_confirm_delete.html', context)

# =============================================================================
# Services Success VIEWS
# =============================================================================
@rbac_permission_required('company_app.view_services_success')
def services_success_list(request):
    """
    Services Success list - accessible to users with view_services_success permission
    """
    context = {
        'page_title': 'Services Success List',
        'breadcrumb_active': 'Services Success List'
    }
    return render(request, 'company/services_success_list.html', context)

@rbac_permission_required('company_app.view_services_success')
def services_success_datatables_api(request):
    """
    Datatables API for services success
    """
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            services_success = Services_success.objects.all().select_related('service')
        else:
            services_success = Services_success.objects.filter(status=True).select_related('service')
        
        # Total records count
        total_records = services_success.count()
        
        # Search functionality
        if search_value:
            services_success = services_success.filter(
                Q(title__icontains=search_value) |
                Q(icon__icontains=search_value) |
                Q(success__icontains=search_value) |
                Q(service__title__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = services_success.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'icon', 
            '2': 'service__title',
            '3': 'success',
            '4': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'title')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        services_success = services_success.order_by(order_field)
        
        # Pagination
        services_success = services_success[start:start + length]
        
        # Prepare data for response - FIXED DATA STRUCTURE
        data = []
        for service_success in services_success:
            # Render icon
            icon_html = f'<i class="{service_success.icon} fa-lg text-primary"></i> <span class="ms-2">{service_success.icon}</span>' if service_success.icon else '<span class="text-muted">No icon</span>'
            
            # Render service relationship
            service_html = f'<span class="badge bg-info">{service_success.service.title}</span>' if service_success.service else '<span class="text-muted">No service</span>'
            
            # Render success value
            success_html = f'<span class="fw-bold text-success">{service_success.success}</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if service_success.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render actions - with permission checks
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has view, edit, or delete permissions
            can_view = has_company_permission(request.user, 'company_app.view_services_success')
            can_edit = has_company_permission(request.user, 'company_app.change_services_success')
            can_delete = has_company_permission(request.user, 'company_app.delete_services_success')
            
            if can_view or can_edit or can_delete:
                actions_buttons = []
                
                if can_view:
                    details_url = reverse('company_app:services_success_details', args=[service_success.pk])
                    actions_buttons.append(
                        f'<a href="{details_url}" class="btn btn-outline-info btn-sm" '
                        f'data-bs-toggle="tooltip" title="View Details">'
                        f'<i class="fas fa-eye"></i></a>'
                    )
                
                if can_edit:
                    edit_url = reverse('company_app:services_success_edit', args=[service_success.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Service Success">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:services_success_delete', args=[service_success.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this service success?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Service Success">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            # FIXED: Ensure the data structure matches DataTables columns
            data.append({
                'title': service_success.title,
                'icon': icon_html,
                'service': service_html,
                'success': success_html,
                'status': status_html,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in services_success_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        }, status=500)
    
@rbac_permission_required('company_app.view_services_success')
def services_success_details(request, pk):
    """View service success details"""
    service_success = get_object_or_404(Services_success, pk=pk)
    
    context = {
        'service_success': service_success,
        'page_title': f'Service Success Details - {service_success.title}',
        'breadcrumb_active': 'Service Success Details'
    }
    return render(request, 'company/services_success_details.html', context)

@rbac_permission_required('company_app.add_services_success')
def services_success_create(request):
    """Create new service success"""
    if request.method == 'POST':
        form = ServiceSuccessForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service success created successfully!')
            return redirect('company_app:services_success_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceSuccessForm()
    
    context = {
        'form': form,
        'page_title': 'Create Service Success',
        'breadcrumb_active': 'Create Service Success',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/services_success_form.html', context)

@rbac_permission_required('company_app.change_services_success')
def services_success_edit(request, pk):
    """Edit existing service success"""
    service_success = get_object_or_404(Services_success, pk=pk)
    
    if request.method == 'POST':
        form = ServiceSuccessForm(request.POST, request.FILES, instance=service_success)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service success updated successfully!')
            return redirect('company_app:services_success_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceSuccessForm(instance=service_success)
    
    context = {
        'form': form,
        'service_success': service_success,
        'page_title': f'Edit Service Success - {service_success.title}',
        'breadcrumb_active': 'Edit Service Success',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/services_success_form.html', context)

@rbac_permission_required('company_app.delete_services_success')
def services_success_delete(request, pk):
    """Delete service success"""
    service_success = get_object_or_404(Services_success, pk=pk)
    
    if request.method == 'POST':
        service_success_name = service_success.title
        service_success.delete()
        messages.success(request, f'Service success "{service_success_name}" deleted successfully!')
        return redirect('company_app:services_success_list')
    
    context = {
        'service_success': service_success,
        'page_title': 'Delete Service Success',
        'breadcrumb_active': 'Delete Service Success'
    }
    return render(request, 'company/services_success_confirm_delete.html', context)




# =============================================================================
# TESTIMONIAL VIEWS
# =============================================================================

@rbac_permission_required('company_app.view_testimonials')
def testimonial_list(request):
    """Testimonial list"""
    context = {
        'page_title': 'Testimonials List',
        'breadcrumb_active': 'Testimonials List'
    }
    return render(request, 'company/testimonial_list.html', context)

@rbac_permission_required('company_app.view_testimonials')
def testimonial_datatables_api(request):
    """Datatables API for testimonials"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            testimonials = Testimonials.objects.all()
        else:
            testimonials = Testimonials.objects.filter(status=True)
        
        # Total records count
        total_records = testimonials.count()
        
        # Search functionality
        if search_value:
            testimonials = testimonials.filter(
                Q(name__icontains=search_value) |
                Q(designation__icontains=search_value) |
                Q(message__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = testimonials.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'name',
            '1': 'designation', 
            '2': 'message',
            '3': 'rating',
            '4': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'name')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        testimonials = testimonials.order_by(order_field)
        
        # Pagination
        testimonials = testimonials[start:start + length]
        
        # Prepare data for response
        data = []
        for testimonial in testimonials:
            # Render message with truncation
            plain_text = strip_tags(testimonial.message)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            message_html = f'<span class="message-text" data-bs-toggle="tooltip" title="{plain_text}">{truncated}</span>'
            
            # Render image with thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if testimonial.image:
                image_html = f'''
                    <img src="{testimonial.image.url}" alt="{testimonial.name}" 
                         class="img-thumbnail testimonial-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            
            # Render rating as stars
            rating_html = ''
            for i in range(1, 6):
                if i <= testimonial.rating:
                    rating_html += '<i class="fas fa-star text-warning"></i>'
                else:
                    rating_html += '<i class="far fa-star text-warning"></i>'
            rating_html = f'<div class="rating-stars">{rating_html}</div>'
            
            # Render designation
            designation_html = testimonial.designation if testimonial.designation else '<span class="text-muted">Not specified</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if testimonial.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_company_permission(request.user, 'company_app.change_testimonials')
            can_delete = has_company_permission(request.user, 'company_app.delete_testimonials')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('company_app:testimonial_edit', args=[testimonial.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Testimonial">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:testimonial_delete', args=[testimonial.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this testimonial?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Testimonial">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'image': image_html,
                'name': testimonial.name,
                'designation': designation_html,
                'message': message_html,
                'rating': rating_html,
                'status': status_html,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in testimonial_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('company_app.add_testimonials')
def testimonial_create(request):
    """Create testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial created successfully!')
            return redirect('company_app:testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
        'page_title': 'Create Testimonial',
        'breadcrumb_active': 'Create Testimonial',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/testimonial_form.html', context)

@rbac_permission_required('company_app.change_testimonials')
def testimonial_edit(request, pk):
    """Edit testimonial"""
    testimonial = get_object_or_404(Testimonials, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('company_app:testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {
        'form': form,
        'testimonial': testimonial,
        'page_title': 'Edit Testimonial',
        'breadcrumb_active': 'Edit Testimonial',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/testimonial_form.html', context)

@rbac_permission_required('company_app.delete_testimonials')
def testimonial_delete(request, pk):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonials, pk=pk)
    
    if request.method == 'POST':
        testimonial_name = testimonial.name
        testimonial.delete()
        messages.success(request, f'Testimonial "{testimonial_name}" deleted successfully!')
        return redirect('company_app:testimonial_list')
    
    context = {
        'testimonial': testimonial,
        'page_title': 'Delete Testimonial',
        'breadcrumb_active': 'Delete Testimonial'
    }
    return render(request, 'company/testimonial_confirm_delete.html', context)

# =============================================================================
# PROJECT DONE VIEWS
# =============================================================================
@rbac_permission_required('company_app.view_project_done')
def project_done_list(request):
    """Project done list"""
    # Get active categories for filter dropdown
    categories = Category.objects.filter(status=True)
    
    context = {
        'page_title': 'Projects Done List',
        'breadcrumb_active': 'Projects Done List',
        'categories': categories
    }
    return render(request, 'company/project_done_list.html', context)

@rbac_permission_required('company_app.view_project_done')
def project_done_datatables_api(request):
    """Datatables API for projects done"""
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        service_id = request.GET.get('service_id')
        category_id = request.GET.get('category_id')  # New category filter
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            projects = Project_done.objects.all().select_related('service', 'category')
        else:
            projects = Project_done.objects.filter(status=True).select_related('service', 'category')
        
        # Filter by service if service_id is provided
        if service_id:
            projects = projects.filter(service_id=service_id)
        
        # Filter by category if category_id is provided
        if category_id:
            projects = projects.filter(category_id=category_id)
        
        # Total records count
        total_records = projects.count()
        
        # Search functionality
        if search_value:
            projects = projects.filter(
                Q(title__icontains=search_value) |
                Q(company__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(service__title__icontains=search_value) |
                Q(category__title__icontains=search_value)  # Added category search
            )
        
        # Filtered records count
        filtered_records = projects.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'company', 
            '2': 'service__title',
            '3': 'category__title',  # Added category ordering
            '4': 'created_at',
            '5': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        projects = projects.order_by(order_field)
        
        # Pagination
        projects = projects[start:start + length]
        
        # Prepare data for response
        data = []
        for project in projects:
            # Render description with truncation
            plain_text = strip_tags(project.description)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            description_html = f'<span class="description-text" data-bs-toggle="tooltip" title="{plain_text}">{truncated}</span>'
            
            # Render project image with thumbnail
            project_image_html = '<span class="text-muted">No image</span>'
            if project.image:
                project_image_html = f'''
                    <img src="{project.image.url}" alt="{project.title}" 
                         class="img-thumbnail project-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            
            # Render company logo with thumbnail
            logo_html = '<span class="text-muted">No logo</span>'
            if project.logo:
                logo_html = f'''
                    <img src="{project.logo.url}" alt="{project.company}" 
                         class="img-thumbnail logo-thumbnail" 
                         style="width: 40px; height: 40px; object-fit: contain;">
                '''
            
            # Render service name
            service_html = f'<span class="badge bg-primary">{project.service.title}</span>'
            
            # Render category name
            category_html = '<span class="text-muted">No category</span>'
            if project.category:
                category_html = f'<span class="badge bg-info">{project.category.title}</span>'
            
            # Render live link
            live_link_html = '<span class="text-muted">No link</span>'
            if project.live_link:
                live_link_html = f'''
                    <a href="{project.live_link}" target="_blank" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-external-link-alt"></i> Visit
                    </a>
                '''
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if project.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render created date
            created_date = project.created_at.strftime('%Y-%m-%d %H:%M')
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_company_permission(request.user, 'company_app.change_project_done')
            can_delete = has_company_permission(request.user, 'company_app.delete_project_done')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('company_app:project_done_edit', args=[project.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Project">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:project_done_delete', args=[project.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this project?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Project">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'title': project.title,
                'company': project.company,
                'service': service_html,
                'category': category_html,  # Added category column
                'description': description_html,
                'project_image': project_image_html,
                'company_logo': logo_html,
                'live_link': live_link_html,
                'created_at': created_date,
                'status': status_html,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in project_done_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('company_app.add_project_done')
def project_done_create(request):
    """Create project done"""
    if request.method == 'POST':
        form = ProjectDoneForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Project created successfully!')
                return redirect('company_app:project_done_list')
            except Exception as e:
                messages.error(request, f'Error creating project: {str(e)}')
        else:
            # Debug form errors
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectDoneForm()
    
    context = {
        'form': form,
        'page_title': 'Create Project',
        'breadcrumb_active': 'Create Project',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/project_done_form.html', context)

@rbac_permission_required('company_app.change_project_done')
def project_done_edit(request, pk):
    """Edit project done"""
    project = get_object_or_404(Project_done, pk=pk)
    
    if request.method == 'POST':
        form = ProjectDoneForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Project updated successfully!')
                return redirect('company_app:project_done_list')
            except Exception as e:
                messages.error(request, f'Error updating project: {str(e)}')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectDoneForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'page_title': f'Update Project - {project.title}',
        'breadcrumb_active': 'Update Project',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/project_done_form.html', context)

@rbac_permission_required('company_app.delete_project_done')
def project_done_delete(request, pk):
    """Delete project done"""
    project = get_object_or_404(Project_done, pk=pk)
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" deleted successfully!')
        return redirect('company_app:project_done_list')
    
    context = {
        'project': project,
        'page_title': 'Delete Project',
        'breadcrumb_active': 'Delete Project'
    }
    return render(request, 'company/project_done_confirm_delete.html', context)

# =============================================================================
# SERVICES TESTIMONIAL VIEWS
# =============================================================================

def has_services_testimonial_permission(user, permission_codename):
    """
    Check if user has specific permission for services testimonials
    """
    if user.is_superuser:
        return True
    return user.has_perm(f'company_app.{permission_codename}')

# Helper function to get queryset based on user permissions
def get_services_testimonial_queryset(user):
    """
    Return appropriate queryset based on user permissions
    """
    if user.is_superuser:
        return Services_testimonial.objects.all()
    elif has_services_testimonial_permission(user, 'view_services_testimonial'):
        return Services_testimonial.objects.all()
    else:
        return Services_testimonial.objects.filter(status=True)

@rbac_permission_required('company_app.view_services_testimonial')
def services_testimonial_list(request):
    """Services testimonial list view"""
    context = {
        'page_title': 'Services Testimonials',
        'breadcrumb_active': 'Services Testimonials',
        'can_add_services_testimonial': has_services_testimonial_permission(request.user, 'add_services_testimonial'),
    }
    return render(request, 'company/services_testimonial_list.html', context)

@rbac_permission_required('company_app.view_services_testimonial')
def servicestestimonial_list(request):
    """Services testimonial list view"""
    context = {
        'page_title': 'Services Testimonials',
        'breadcrumb_active': 'Services Testimonials',
        'can_add_services_testimonial': has_services_testimonial_permission(request.user, 'add_services_testimonial'),
    }
    return render(request, 'company/servicestestimonial_list.html', context)

@rbac_permission_required('company_app.view_services_testimonial')
def services_testimonial_datatables_api(request):
    """Datatables API for services testimonials"""
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        service_id = request.GET.get('service_id')  # Get service_id from request
        
        # Get appropriate queryset based on user permissions
        services_testimonials = get_services_testimonial_queryset(request.user)
        
        # Filter by service if service_id is provided
        if service_id:
            services_testimonials = services_testimonials.filter(service_id=service_id)
        
        # Total records count
        total_records = services_testimonials.count()
        
        # Search functionality
        if search_value:
            services_testimonials = services_testimonials.filter(
                Q(name__icontains=search_value) |
                Q(designation__icontains=search_value) |
                Q(message__icontains=search_value) |
                Q(service__title__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = services_testimonials.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'name',
            '1': 'service__title',
            '2': 'designation', 
            '3': 'rating',
            '4': 'status',
            '5': 'created_at'
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        services_testimonials = services_testimonials.order_by(order_field)
        
        # Pagination
        services_testimonials = services_testimonials[start:start + length]
        
        # Prepare data for response
        data = []
        for testimonial in services_testimonials:
            # Render message with truncation
            plain_text = strip_tags(testimonial.message)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            message_html = f'''
                <span class="message-tooltip" 
                      data-bs-toggle="tooltip" 
                      title="{plain_text}"
                      style="cursor: pointer;">
                    {truncated}
                </span>
            '''
            
            # Render image with thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if testimonial.image:
                image_html = f'''
                    <img src="{testimonial.image.url}" alt="{testimonial.name}" 
                         class="img-thumbnail testimonial-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover; cursor: pointer;"
                         onclick="viewImage('{testimonial.image.url}', '{testimonial.name}')">
                '''
            
            # Render rating as stars
            rating_html = testimonial.star_display
            rating_html = f'<div class="rating-stars" data-bs-toggle="tooltip" title="{testimonial.rating} stars">{rating_html}</div>'
            
            # Render service
            service_html = f'<span class="badge bg-primary">{testimonial.service.title}</span>'
            
            # Render designation
            designation_html = testimonial.designation if testimonial.designation else '<span class="text-muted">Not specified</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if testimonial.status else '''
                <span class="badge bg-secondary rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render created date
            created_html = testimonial.created_at.strftime('%Y-%m-%d %H:%M')
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_services_testimonial_permission(request.user, 'change_services_testimonial')
            can_delete = has_services_testimonial_permission(request.user, 'delete_services_testimonial')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                # View button (always available)
                view_url = reverse('company_app:services_testimonial_detail', args=[testimonial.pk])
                actions_buttons.append(
                    f'<a href="{view_url}" class="btn btn-outline-info btn-sm" '
                    f'data-bs-toggle="tooltip" title="View Details">'
                    f'<i class="fas fa-eye"></i></a>'
                )
                
                if can_edit:
                    edit_url = reverse('company_app:services_testimonial_edit', args=[testimonial.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-warning btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Testimonial">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:services_testimonial_delete', args=[testimonial.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete testimonial from {testimonial.name}?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Testimonial">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'image': image_html,
                'name': f'<strong>{testimonial.name}</strong>',
                'service': service_html,
                'designation': designation_html,
                'message': message_html,
                'rating': rating_html,
                'status': status_html,
                'created_at': f'<small class="text-muted">{created_html}</small>',
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in services_testimonial_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'An error occurred while processing your request.'
        }, status=500)

@rbac_permission_required('company_app.add_services_testimonial')
def services_testimonial_create(request):
    """Create services testimonial"""
    # Get service_id from query parameter if available
    service_id = request.GET.get('service')
    
    if request.method == 'POST':
        form = ServicesTestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.save()
            messages.success(request, 'Service testimonial created successfully!')
            
            # Redirect based on where the user came from
            if 'service' in request.GET:
                return redirect('company_app:service_details', pk=service_id)
            return redirect('company_app:services_testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        form = ServicesTestimonialForm(initial=initial_data)
    
    context = {
        'form': form,
        'page_title': 'Create Service Testimonial',
        'breadcrumb_active': 'Create Service Testimonial',
    }
    return render(request, 'company/services_testimonial_form.html', context)

@rbac_permission_required('company_app.change_services_testimonial')
def services_testimonial_edit(request, pk):
    """Edit services testimonial"""
    testimonial = get_object_or_404(Services_testimonial, pk=pk)
    
    if request.method == 'POST':
        form = ServicesTestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service testimonial updated successfully!')
            return redirect('company_app:services_testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServicesTestimonialForm(instance=testimonial)
    
    context = {
        'form': form,
        'testimonial': testimonial,
        'page_title': f'Edit Testimonial - {testimonial.name}',
        'breadcrumb_active': 'Edit Testimonial',
    }
    return render(request, 'company/services_testimonial_form.html', context)

@rbac_permission_required('company_app.delete_services_testimonial')
def services_testimonial_delete(request, pk):
    """Delete services testimonial"""
    testimonial = get_object_or_404(Services_testimonial, pk=pk)
    
    if request.method == 'POST':
        testimonial_name = testimonial.name
        testimonial.delete()
        messages.success(request, f'Service testimonial "{testimonial_name}" deleted successfully!')
        return redirect('company_app:services_testimonial_list')
    
    context = {
        'testimonial': testimonial,
        'page_title': 'Delete Service Testimonial',
        'breadcrumb_active': 'Delete Testimonial'
    }
    return render(request, 'company/services_testimonial_confirm_delete.html', context)

def services_testimonial_detail(request, pk):
    """Services testimonial detail view"""
    testimonial = get_object_or_404(Services_testimonial, pk=pk)
    
    context = {
        'testimonial': testimonial,
        'page_title': f'Testimonial - {testimonial.name}',
    }
    return render(request, 'company/services_testimonial_detail.html', context)

@login_required
def toggle_services_testimonial_status(request, pk):
    """Toggle services testimonial status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            testimonial = get_object_or_404(Services_testimonial, pk=pk)
            
            # Check if user has permission
            if not has_services_testimonial_permission(request.user, 'change_services_testimonial'):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this testimonial status.'
                }, status=403)
            
            # Toggle status
            testimonial.status = not testimonial.status
            testimonial.save()
            
            return JsonResponse({
                'success': True,
                'new_status': testimonial.status,
                'status_display': 'Active' if testimonial.status else 'Inactive',
                'message': f'Testimonial status updated to {"Active" if testimonial.status else "Inactive"} successfully!'
            })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Service-specific testimonial views
@rbac_permission_required('company_app.view_services_testimonial')
def service_testimonials_list(request, service_id):
    """List testimonials for a specific service"""
    service = get_object_or_404(Services, pk=service_id)
    
    context = {
        'service': service,
        'page_title': f'Testimonials - {service.title}',
        'breadcrumb_active': f'Testimonials for {service.title}',
    }
    return render(request, 'company/service_testimonials_list.html', context)

# =============================================================================
# SERVICES FAQ VIEWS
# =============================================================================

def has_services_faq_permission(user, permission_codename):
    """
    Check if user has specific permission for services FAQs
    """
    if user.is_superuser:
        return True
    return user.has_perm(f'company_app.{permission_codename}')

# Helper function to get queryset based on user permissions
def get_services_faq_queryset(user):
    """
    Return appropriate queryset based on user permissions
    """
    if user.is_superuser:
        return Services_faq.objects.all()
    elif has_services_faq_permission(user, 'view_services_faq'):
        return Services_faq.objects.all()
    else:
        return Services_faq.objects.filter(status='published')

@rbac_permission_required('company_app.view_services_faq')
def services_faq_list(request):
    """Services FAQ list view"""
    context = {
        'page_title': 'Services FAQs',
        'breadcrumb_active': 'Services FAQs',
        'can_add_services_faq': has_services_faq_permission(request.user, 'add_services_faq'),
    }
    return render(request, 'company/services_faq_list.html', context)

@rbac_permission_required('company_app.view_services_faq')
def services_faq_datatables_api(request):
    """Datatables API for services FAQs"""
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        service_id = request.GET.get('service_id')  # Get service_id from request
        
        # Get appropriate queryset based on user permissions
        services_faqs = get_services_faq_queryset(request.user)
        
        # Filter by service if service_id is provided
        if service_id:
            services_faqs = services_faqs.filter(service_id=service_id)
        
        # Total records count
        total_records = services_faqs.count()
        
        # Search functionality
        if search_value:
            services_faqs = services_faqs.filter(
                Q(question__icontains=search_value) |
                Q(answer__icontains=search_value) |
                Q(service__title__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = services_faqs.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'question',
            '1': 'service__title',
            '2': 'status',
            '3': 'created_at',
            '4': 'updated_at'
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        services_faqs = services_faqs.order_by(order_field)
        
        # Pagination
        services_faqs = services_faqs[start:start + length]
        
        # Prepare data for response
        data = []
        for faq in services_faqs:
            # Render question with truncation
            plain_question = strip_tags(faq.question)
            truncated_question = plain_question[:60] + "..." if len(plain_question) > 60 else plain_question
            question_html = f'''
                <span class="question-tooltip" 
                      data-bs-toggle="tooltip" 
                      title="{plain_question}"
                      style="cursor: pointer; font-weight: 500;">
                    {truncated_question}
                </span>
            '''
            
            # Render answer with truncation
            plain_answer = strip_tags(faq.answer)
            truncated_answer = plain_answer[:80] + "..." if len(plain_answer) > 80 else plain_answer
            answer_html = f'''
                <span class="answer-tooltip" 
                      data-bs-toggle="tooltip" 
                      title="{plain_answer}"
                      style="cursor: pointer;">
                    {truncated_answer}
                </span>
            '''
            
            # Render service
            service_html = f'<span class="badge bg-info">{faq.service.title}</span>'
            
            # Render status with appropriate badges
            if faq.status == 'published':
                status_html = '''
                    <span class="badge bg-success">
                        <i class="fas fa-check-circle me-1"></i>Published
                    </span>
                '''
            elif faq.status == 'draft':
                status_html = '''
                    <span class="badge bg-warning text-dark">
                        <i class="fas fa-pencil-alt me-1"></i>Draft
                    </span>
                '''
            else:
                status_html = f'''
                    <span class="badge bg-secondary">
                        <i class="fas fa-question-circle me-1"></i>{faq.status.title()}
                    </span>
                '''
            
            # Render dates
            created_date = faq.created_at.strftime('%Y-%m-%d %H:%M')
            updated_date = faq.updated_at.strftime('%Y-%m-%d %H:%M')
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_services_faq_permission(request.user, 'change_services_faq')
            can_delete = has_services_faq_permission(request.user, 'delete_services_faq')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                # View detail button
                detail_url = reverse('company_app:services_faq_detail', args=[faq.pk])
                actions_buttons.append(
                    f'<a href="{detail_url}" class="btn btn-outline-info btn-sm" '
                    f'data-bs-toggle="tooltip" title="View Details">'
                    f'<i class="fas fa-eye"></i></a>'
                )
                
                if can_edit:
                    edit_url = reverse('company_app:services_faq_edit', args=[faq.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit FAQ">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                    
                if can_delete:
                    delete_url = reverse('company_app:services_faq_delete', args=[faq.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this FAQ?\')" '
                        f'data-bs-toggle="tooltip" title="Delete FAQ">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'question': question_html,
                'service': service_html,
                'answer': answer_html,
                'status': status_html,
                'created_at': created_date,
                'updated_at': updated_date,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in services_faq_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'An error occurred while processing your request.'
        }, status=500)

@rbac_permission_required('company_app.add_services_faq')
def services_faq_create(request):
    """Create services FAQ"""
    # Get service_id from query parameter if available
    service_id = request.GET.get('service')
    
    if request.method == 'POST':
        form = ServicesFaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.save()
            messages.success(request, 'Service FAQ created successfully!')
            return redirect('company_app:services_faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        form = ServicesFaqForm(initial=initial_data)
    
    context = {
        'form': form,
        'page_title': 'Create Service FAQ',
        'breadcrumb_active': 'Create Service FAQ',
    }
    return render(request, 'company/services_faq_form.html', context)

@rbac_permission_required('company_app.change_services_faq')
def services_faq_edit(request, pk):
    """Edit services FAQ"""
    faq = get_object_or_404(Services_faq, pk=pk)
    
    if request.method == 'POST':
        form = ServicesFaqForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service FAQ updated successfully!')
            return redirect('company_app:services_faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServicesFaqForm(instance=faq)
    
    context = {
        'form': form,
        'faq': faq,
        'page_title': f'Edit FAQ',
        'breadcrumb_active': 'Edit FAQ',
    }
    return render(request, 'company/services_faq_form.html', context)

@rbac_permission_required('company_app.delete_services_faq')
def services_faq_delete(request, pk):
    """Delete services FAQ"""
    faq = get_object_or_404(Services_faq, pk=pk)
    
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'Service FAQ deleted successfully!')
        return redirect('company_app:services_faq_list')
    
    context = {
        'faq': faq,
        'page_title': 'Delete Service FAQ',
        'breadcrumb_active': 'Delete FAQ'
    }
    return render(request, 'company/services_faq_confirm_delete.html', context)

def services_faq_detail(request, pk):
    """Services FAQ detail view"""
    faq = get_object_or_404(Services_faq, pk=pk)
    
    # Check if user can view non-published FAQs
    if faq.status != 'published' and not has_services_faq_permission(request.user, 'view_services_faq'):
        raise PermissionDenied("You don't have permission to view this FAQ.")
    
    context = {
        'faq': faq,
        'page_title': f'FAQ - {faq.question}',
        'can_edit_services_faq': has_services_faq_permission(request.user, 'change_services_faq'),
        'can_delete_services_faq': has_services_faq_permission(request.user, 'delete_services_faq'),
    }
    return render(request, 'company/services_faq_detail.html', context)

@login_required
def toggle_services_faq_status(request, pk):
    """Toggle services FAQ status between draft and published"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            faq = Services_faq.objects.get(pk=pk)
            
            # Check if user has permission to change FAQ status
            if not has_services_faq_permission(request.user, 'change_services_faq'):
                return JsonResponse({
                    'success': False, 
                    'error': 'You do not have permission to change FAQ status.'
                }, status=403)
            
            # Toggle status between draft and published
            if faq.status == 'draft':
                faq.status = 'published'
                faq.save()
                return JsonResponse({
                    'success': True, 
                    'new_status': 'published',
                    'new_status_display': 'Published',
                    'new_badge_class': 'bg-success',
                    'new_icon': 'fa-eye-slash',
                    'new_title': 'Unpublish',
                    'new_btn_class': 'btn-outline-warning',
                    'message': 'FAQ published successfully!'
                })
            elif faq.status == 'published':
                faq.status = 'draft'
                faq.save()
                return JsonResponse({
                    'success': True, 
                    'new_status': 'draft',
                    'new_status_display': 'Draft',
                    'new_badge_class': 'bg-warning text-dark',
                    'new_icon': 'fa-eye',
                    'new_title': 'Publish',
                    'new_btn_class': 'btn-outline-success',
                    'message': 'FAQ unpublished successfully!'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Cannot toggle status from current state'
                })
                
        except Services_faq.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'FAQ not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request'
    })

# Service-specific FAQ views
@rbac_permission_required('company_app.view_services_faq')
def service_faqs_list(request, service_id):
    """List FAQs for a specific service"""
    service = get_object_or_404(Services, pk=service_id)
    
    context = {
        'service': service,
        'page_title': f'FAQs - {service.title}',
        'breadcrumb_active': f'FAQs for {service.title}',
    }
    return render(request, 'company/service_faqs_list.html', context)

# =============================================================================
# CATEGORY VIEWS
# =============================================================================
@rbac_permission_required('company_app.view_category')
def category_list(request):
    """Category list view"""
    context = {
        'page_title': 'Categories',
        'breadcrumb_active': 'Categories',
        'breadcrumb_icon': 'grid'
    }
    return render(request, 'company/category_list.html', context)

@rbac_permission_required('company_app.view_category')
def category_datatables_api(request):
    """Datatables API for categories"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            categories = Category.objects.all()
        else:
            categories = Category.objects.filter(status=True)
        
        # Total records count
        total_records = categories.count()
        
        # Search functionality
        if search_value:
            categories = categories.filter(
                Q(title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(slug__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = categories.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'description', 
            '2': 'ordering',
            '3': 'status',
            '4': 'created_at'
        }
        
        order_field = column_map.get(order_column_index, 'ordering')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        categories = categories.order_by(order_field)
        
        # Pagination
        categories = categories[start:start + length]
        
        # Prepare data for response
        data = []
        for category in categories:
            # Render image with thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if category.image:
                image_html = f'''
                    <img src="{category.image.url}" alt="{category.title}" 
                         class="img-thumbnail category-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            else:
                image_html = f'''
                    <img src="{category.get_image_url()}" alt="{category.title}" 
                         class="img-thumbnail category-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            
            # Render description with truncation
            description_text = strip_tags(category.description) if category.description else "No description"
            truncated = description_text[:80] + "..." if len(description_text) > 80 else description_text
            description_html = f'<span class="description-text" data-bs-toggle="tooltip" title="{description_text}">{truncated}</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if category.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render ordering
            ordering_html = f'<span class="badge bg-primary">{category.ordering}</span>'
            
            # Render created date
            created_date = category.created_at.strftime('%Y-%m-%d %H:%M')
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_company_permission(request.user, 'company_app.change_category')
            can_delete = has_company_permission(request.user, 'company_app.delete_category')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('company_app:category_edit', args=[category.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Category">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('company_app:category_delete', args=[category.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this category?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Category">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'image': image_html,
                'title': category.title,
                'description': description_html,
                'ordering': ordering_html,
                'status': status_html,
                'created_at': created_date,
                'actions': actions_html,
            })
        
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
        
        return JsonResponse(response)
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in category_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('company_app.add_category')
def category_create(request):
    """Create category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            # Slug will be auto-generated in the save method
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('company_app:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'page_title': 'Create Category',
        'breadcrumb_active': 'Create Category',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'company/category_form.html', context)

@rbac_permission_required('company_app.change_category')
def category_edit(request, pk):
    """Edit category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('company_app:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'page_title': 'Edit Category',
        'breadcrumb_active': 'Edit Category',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'company/category_form.html', context)

@rbac_permission_required('company_app.delete_category')
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_title = category.title
        category.delete()
        messages.success(request, f'Category "{category_title}" deleted successfully!')
        return redirect('company_app:category_list')
    
    context = {
        'category': category,
        'page_title': 'Delete Category',
        'breadcrumb_active': 'Delete Category'
    }
    return render(request, 'company/category_confirm_delete.html', context)

