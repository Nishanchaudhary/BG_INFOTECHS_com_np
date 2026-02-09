from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils.html import strip_tags
from .models import Package,PlanSubscriber,CustomPackage
from .forms import PackageForm
from bg_app.decorators import role_required,rbac_permission_required

# =============================================================================
# PACKAGE VIEWS
# =============================================================================
def has_company_permission(user, permission_codename):
    """
    Check if user has specific company permission
    """
    return user.is_superuser or (user.role and user.role.name == 'admin') or user.has_perm(permission_codename)

@rbac_permission_required('package_app.view_package')
def package_list(request):
    """Package list"""
    context = {
        'page_title': 'Packages List',
        'breadcrumb_active': 'Packages List'
    }
    return render(request, 'package/package_list.html', context)

@rbac_permission_required('package_app.view_package')
def package_datatables_api(request):
    """Datatables API for packages"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            packages = Package.objects.all()
        else:
            packages = Package.objects.filter(status=True)
        
        # Total records count
        total_records = packages.count()
        
        # Search functionality
        if search_value:
            packages = packages.filter(
                Q(title__icontains=search_value) |
                Q(short_desc__icontains=search_value) |
                Q(tags__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = packages.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'title',
            '1': 'month_price', 
            '2': 'year_price',
            '3': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'title')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        packages = packages.order_by(order_field)
        
        # Pagination
        packages = packages[start:start + length]
        
        # Prepare data for response
        data = []
        for package in packages:
            # Render image with thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if package.image:
                image_html = f'''
                    <img src="{package.image.url}" alt="{package.title}" 
                         class="img-thumbnail package-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            
            # Render icon
            icon_html = f'<i class="{package.icon}"></i>' if package.icon else '<span class="text-muted">No icon</span>'
            
            # Render short description with truncation
            short_desc_html = package.short_desc[:80] + "..." if len(package.short_desc) > 80 else package.short_desc
            
            # Render prices
            month_price_html = f'<span class="text-success">₹{package.month_price}/month</span>'
            year_price_html = f'<span class="text-primary">₹{package.year_price}/year</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if package.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render tags
            tags_html = '<span class="text-muted">No tags</span>'
            if package.tags:
                tags_list = package.tags.split(',')
                tags_badges = [f'<span class="badge bg-secondary me-1">{tag.strip()}</span>' for tag in tags_list[:3]]
                tags_html = ''.join(tags_badges)
                if len(tags_list) > 3:
                    tags_html += f'<span class="badge bg-light text-dark">+{len(tags_list)-3} more</span>'
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = has_company_permission(request.user, 'package_app.change_package')
            can_delete = has_company_permission(request.user, 'package_app.delete_package')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('package_app:package_edit', args=[package.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Package">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('package_app:package_delete', args=[package.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this package?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Package">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'icon': icon_html,
                'image': image_html,
                'title': package.title,
                'short_desc': short_desc_html,
                'month_price': month_price_html,
                'year_price': year_price_html,
                'tags': tags_html,
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
        logger.error(f"Error in package_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('package_app.add_package')
def package_create(request):
    """Create package"""
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package created successfully!')
            return redirect('package_app:package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageForm()
    
    context = {
        'form': form,
        'page_title': 'Create Package',
        'breadcrumb_active': 'Create Package',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'package/package_form.html', context)

@rbac_permission_required('package_app.change_package')
def package_edit(request, pk):
    """Edit package"""
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package updated successfully!')
            return redirect('package_app:package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageForm(instance=package)
    
    context = {
        'form': form,
        'package': package,
        'page_title': 'Edit Package',
        'breadcrumb_active': 'Edit Package',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'package/package_form.html', context)

@rbac_permission_required('package_app.delete_package')
def package_delete(request, pk):
    """Delete package"""
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        package_title = package.title
        package.delete()
        messages.success(request, f'Package "{package_title}" deleted successfully!')
        return redirect('package_app:package_list')
    
    context = {
        'package': package,
        'page_title': 'Delete Package',
        'breadcrumb_active': 'Delete Package'
    }
    return render(request, 'package/package_confirm_delete.html', context)


# =============================================================================
# PLAN SUBSCRIBER VIEWS
# =============================================================================


@rbac_permission_required('package_app.view_plansubscriber')
def planSubscriber_list(request):
    """Plan Subscriber list"""
    context = {
        'page_title': 'Plan Subscribers List',
        'breadcrumb_active': 'Plan Subscribers List'
    }
    return render(request, 'package/planSubscriber_list.html', context)


@rbac_permission_required('package_app.view_plansubscriber')
def planSubscriber_datatable_api(request):
    """Datatables API for plan subscribers"""
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        qs = PlanSubscriber.objects.all().select_related('package')

        total_records = qs.count()

        # Search functionality
        if search_value:
            q = Q(name_business_name__icontains=search_value) | \
                Q(email__icontains=search_value) | \
                Q(phone_number__icontains=search_value) | \
                Q(package__title__icontains=search_value)
            qs = qs.filter(q)

        filtered_records = qs.count()

        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        order_columns = ['id', 'name_business_name', 'email', 'phone_number', 'created_at', 'package__title']
        
        try:
            order_column = order_columns[int(order_column_index)]
            if order_direction == 'desc':
                order_column = '-' + order_column
            qs = qs.order_by(order_column)
        except (IndexError, ValueError):
            qs = qs.order_by('-id')

        # Pagination
        qs = qs[start:start + length]

        data = []
        for obj in qs:
            # Use the actual field name from model
            name = obj.name_business_name
            email = obj.email
            phone = obj.phone_number
            package_title = obj.package.title if obj.package else ''
            created = obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else ''

            # Actions (delete)
            actions_html = '<span class="text-muted">No actions</span>'
            # Assuming you have proper permission checking
            can_delete = True  # Replace with your actual permission check
            if can_delete:
                delete_url = reverse('package_app:planSubscriber_delete', args=[obj.pk])
                actions_html = (
                    f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm delete-btn" '
                    f'data-bs-toggle="tooltip" title="Delete Subscriber">'
                    f'<i class="fas fa-trash"></i></a>'
                )

            data.append({
                'id': obj.pk,
                'name': str(name),
                'email': str(email),
                'phone_number': str(phone),
                'package': str(package_title),
                'created_at': str(created),
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
        print(f"Error in planSubscriber_datatable_api: {str(e)}")  # For debugging
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        }, status=500)


@rbac_permission_required('package_app.delete_plansubscriber')
def planSubscriber_delete(request, pk):
    """Delete plan subscriber"""
    subscriber = get_object_or_404(PlanSubscriber, pk=pk)

    if request.method == 'POST':
        name = getattr(subscriber, 'name', '') or getattr(subscriber, 'email', str(subscriber))
        subscriber.delete()
        messages.success(request, f'Plan Subscriber "{name}" deleted successfully!')
        return redirect('package_app:planSubscriber_list')

    context = {
        'subscriber': subscriber,
        'page_title': 'Delete Plan Subscriber',
        'breadcrumb_active': 'Delete Plan Subscriber'
    }
    return render(request, 'package/planSubscriber_confirm_delete.html', context)


# =============================================================================
# CUSTOM PACKAGE VIEWS
# =============================================================================
@rbac_permission_required('package_app.view_custompackage')
def custom_package_list(request):
    """Custom Package list"""
    context = {
        'page_title': 'Custom Packages List',
        'breadcrumb_active': 'Custom Packages List'
    }
    return render(request, 'package/custom_package_list.html', context)


@rbac_permission_required('package_app.view_custompackage')
def custom_package_datatables_api(request):
    """Datatables API for custom packages"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset
        custom_packages = CustomPackage.objects.all()
        
        # Total records count
        total_records = custom_packages.count()
        
        # Search functionality
        if search_value:
            custom_packages = custom_packages.filter(
                Q(name_business_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(business_category__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = custom_packages.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'name_business_name',
            '1': 'email', 
            '2': 'business_category',
            '3': 'created_at'
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        custom_packages = custom_packages.order_by(order_field)
        
        # Pagination
        custom_packages = custom_packages[start:start + length]
        
        # Prepare data for response
        data = []
        for cp in custom_packages:
            data.append({
                'id': cp.id,  # Add ID field for delete operations
                'name_business_name': cp.name_business_name,
                'phone_number': cp.phone_number,
                'email': cp.email,
                'business_category': cp.business_category,
                'no_of_graphics': cp.no_of_graphics,
                'no_of_videos': cp.no_of_videos,
                'created_at': cp.created_at.strftime('%Y-%m-%d %H:%M:%S'),
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
        logger.error(f"Error in custom_package_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': []
        }, status=500)

@rbac_permission_required('package_app.delete_custompackage')
def custom_package_delete(request, pk):
    """Delete custom package"""
    custom_package = get_object_or_404(CustomPackage, pk=pk)
    
    if request.method == 'POST':
        cp_name = custom_package.name_business_name
        custom_package.delete()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Custom Package "{cp_name}" deleted successfully!'
            })
        
        messages.success(request, f'Custom Package "{cp_name}" deleted successfully!')
        return redirect('package_app:custom_package_list')
    
    # For GET requests, render the confirmation page
    context = {
        'custom_package': custom_package,
        'page_title': 'Delete Custom Package',
        'breadcrumb_active': 'Delete Custom Package'
    }
    return render(request, 'package/custom_package_confirm_delete.html', context)
 
