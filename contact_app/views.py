from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.urls import reverse
from bg_app.views import rbac_permission_required
from .models import Branch,Contact
from .forms import BranchForm

# =============================================================================
# BRANCH VIEWS
# =============================================================================

def has_company_permission(user, permission_codename):
    """
    Check if user has specific company permission
    """
    return user.is_superuser or (user.role and user.role.name == 'admin') or user.has_perm(permission_codename)

@rbac_permission_required('contact_app.view_branch')
def branch_list(request):
    """Branch list"""
    context = {
        'page_title': 'Branches List',
        'breadcrumb_active': 'Branches List'
    }
    return render(request, 'contact/branch_list.html', context)

@rbac_permission_required('contact_app.view_branch')
def branch_datatables_api(request):
    """Datatables API for branches"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        
        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            branches = Branch.objects.all()
        else:
            branches = Branch.objects.filter(status=True)
        
        # Total records count
        total_records = branches.count()
        
        # Search functionality
        if search_value:
            branches = branches.filter(
                Q(name__icontains=search_value) |
                Q(address__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(facebook__icontains=search_value) |
                Q(twitter__icontains=search_value) |
                Q(linkedin__icontains=search_value) |
                Q(instagram__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = branches.count()
        
        # Ordering
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        column_map = {
            '0': 'name',
            '1': 'address', 
            '2': 'email',
            '3': 'phone',
            '4': 'office_open',
            '5': 'status'
        }
        
        order_field = column_map.get(order_column_index, 'name')
        if order_direction == 'desc':
            order_field = '-' + order_field
        
        branches = branches.order_by(order_field)
        
        # Pagination
        branches = branches[start:start + length]
        
        # Prepare data for response
        data = []
        for branch in branches:
            # Render description with truncation and HTML safety
            if branch.description:
                plain_text = strip_tags(branch.description)
                truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
                description_html = f'<span class="description-text" data-bs-toggle="tooltip" title="{plain_text}">{truncated}</span>'
            else:
                description_html = '<span class="text-muted">No description</span>'
            
            # Render image with thumbnail
            image_html = '<span class="text-muted">No image</span>'
            if branch.image:
                image_html = f'''
                    <img src="{branch.image.url}" alt="{branch.name}" 
                         class="img-thumbnail branch-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: cover;">
                '''
            
            # Render phone numbers - FIXED: Properly handle multiple phone numbers
            phone_numbers = branch.get_phone_numbers()
            phone_html = '<span class="text-muted">No phone</span>'
            if phone_numbers:
                # Display first 2 phone numbers with proper formatting
                displayed_numbers = []
                for i, number in enumerate(phone_numbers[:2]):
                    displayed_numbers.append(f'<div class="phone-number">{number}</div>')
                
                phone_html = ''.join(displayed_numbers)
                
                # Show count if there are more numbers
                if len(phone_numbers) > 2:
                    phone_html += f'<div class="text-muted small">+{len(phone_numbers)-2} more</div>'
            
            # Render address with truncation
            if branch.address:
                address_truncated = branch.address[:60] + "..." if len(branch.address) > 60 else branch.address
                address_html = f'<span class="address-text" data-bs-toggle="tooltip" title="{branch.address}">{address_truncated}</span>'
            else:
                address_html = '<span class="text-muted">No address</span>'
            
            # Render office hours
            office_html = branch.office_open if branch.office_open else '<span class="text-muted">Not specified</span>'
            
            # Render social media links
            social_media_html = []
            social_platforms = [
                ('facebook', 'fab fa-facebook text-primary', 'Facebook'),
                ('twitter', 'fab fa-twitter text-info', 'Twitter'),
                ('linkedin', 'fab fa-linkedin text-primary', 'LinkedIn'),
                ('instagram', 'fab fa-instagram text-danger', 'Instagram')
            ]
            
            for platform, icon_class, platform_name in social_platforms:
                url = getattr(branch, platform)
                if url and url not in ['', 'https://www.facebook.com/', 'https://www.x.com/', 'https://www.linkedin.com/', 'https://www.instagram.com/']:
                    social_media_html.append(
                        f'<a href="{url}" target="_blank" class="social-icon me-1" '
                        f'data-bs-toggle="tooltip" title="{platform_name}">'
                        f'<i class="{icon_class}"></i></a>'
                    )
            
            if social_media_html:
                social_html = f'<div class="social-links">{"".join(social_media_html)}</div>'
            else:
                social_html = '<span class="text-muted">No social links</span>'
            
            # Render status
            status_html = '''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if branch.status else '''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Render actions
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit and delete permissions
            can_edit = has_company_permission(request.user, 'contact_app.change_branch')
            can_delete = has_company_permission(request.user, 'contact_app.delete_branch')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                # Add edit button if user has permission
                if can_edit:
                    edit_url = reverse('contact_app:branch_edit', args=[branch.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Branch">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                
                # Add delete button if user has permission
                if can_delete:
                    delete_url = reverse('contact_app:branch_delete', args=[branch.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete this branch?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Branch">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'image': image_html,
                'name': branch.name,
                'address': address_html,
                'email': branch.email,
                'phone': phone_html,
                'office_open': office_html,
                'social_media': social_html,
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
        logger.error(f"Error in branch_datatables_api: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })
    
@rbac_permission_required('contact_app.add_branch')
def branch_create(request):
    """Create branch"""
    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES)
        if form.is_valid():
            branch = form.save()
            messages.success(request, f'Branch "{branch.name}" created successfully!')
            return redirect('contact_app:branch_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BranchForm()
    
    context = {
        'form': form,
        'page_title': 'Create Branch',
        'breadcrumb_active': 'Create Branch',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'contact/branch_form.html', context)

@rbac_permission_required('contact_app.change_branch')
def branch_edit(request, pk):
    """Edit branch"""
    branch = get_object_or_404(Branch, pk=pk)
    
    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES, instance=branch)
        if form.is_valid():
            branch = form.save()
            messages.success(request, f'Branch "{branch.name}" updated successfully!')
            return redirect('contact_app:branch_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BranchForm(instance=branch)
    
    context = {
        'form': form,
        'branch': branch,
        'page_title': 'Edit Branch',
        'breadcrumb_active': 'Edit Branch',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'contact/branch_form.html', context)

@rbac_permission_required('contact_app.delete_branch')
def branch_delete(request, pk):
    """Delete branch"""
    branch = get_object_or_404(Branch, pk=pk)
    
    if request.method == 'POST':
        branch_name = branch.name
        branch.delete()
        messages.success(request, f'Branch "{branch_name}" deleted successfully!')
        return redirect('contact_app:branch_list')
    
    context = {
        'branch': branch,
        'page_title': 'Delete Branch',
        'breadcrumb_active': 'Delete Branch'
    }
    return render(request, 'contact/branch_confirm_delete.html', context)

# Contact App...................................................................

@rbac_permission_required('contact_app.view_contact')
def contact_list(request):
    """Contact list"""
    context = {
        'page_title': 'Contacts List',
        'breadcrumb_active': 'Contacts List'
    }
    return render(request, 'contact/contact_list.html', context)

@rbac_permission_required('contact_app.view_contact')
def contact_datatable_api(request):
    """Datatables API for contacts"""
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        # Base queryset - superusers/admin see all, others see only active
        if request.user.is_superuser or (request.user.role and request.user.role.name == 'admin'):
            contacts = Contact.objects.all().select_related('service')
        else:
            contacts = Contact.objects.filter(status=True).select_related('service')

        total_records = contacts.count()

        if search_value:
            contacts = contacts.filter(
                Q(full_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone_number__icontains=search_value) |
                Q(service__title__icontains=search_value) |
                Q(message__icontains=search_value)
            )

        filtered_records = contacts.count()

        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Updated column map with correct field names
        column_map = {
            '0': 'full_name',
            '1': 'email', 
            '2': 'phone_number',
            '3': 'service__title',
            '4': 'message',
            '5': 'status',
            '6': 'is_read',
            '7': 'created_at'
        }

        order_field = column_map.get(order_column_index, 'created_at')
        if order_direction == 'desc':
            order_field = '-' + order_field

        contacts = contacts.order_by(order_field)
        contacts = contacts[start:start + length]

        data = []
        for contact in contacts:
            # Message handling with popup functionality
            message_html = '<span class="text-muted">No message</span>'
            if contact.message:
                short_message = contact.get_short_message(50)
                message_html = f'''
                    <span class="message-text text-primary" style="cursor: pointer;" 
                          data-bs-toggle="modal" data-bs-target="#messageModal"
                          data-full-message="{contact.message}" 
                          data-contact-name="{contact.full_name}">
                        {short_message}
                    </span>
                '''

            # Phone number
            phone_html = f'<div class="phone-number">{contact.phone_number}</div>' if contact.phone_number else '<span class="text-muted">No phone</span>'

            # Service
            service_html = f'<span class="badge bg-info">{contact.service.title}</span>' if contact.service else '<span class="text-muted">No service</span>'

            # Status
            status_html = '''
                <span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Active</span>
            ''' if contact.status else '''
                <span class="badge bg-danger rounded-pill"><i class="fas fa-times-circle me-1"></i>Inactive</span>
            '''

            # Read status
            read_status_html = '''
                <span class="read-status read" data-bs-toggle="tooltip" title="Read">
                    <i class="fas fa-check fa-xs"></i>
                </span>
            ''' if contact.is_read else '''
                <span class="read-status unread" data-bs-toggle="tooltip" title="Unread">
                    <i class="fas fa-envelope fa-xs"></i>
                </span>
            '''

            # Actions - FIXED: Properly generate URLs
            can_edit = has_company_permission(request.user, 'contact_app.change_contact')
            can_delete = has_company_permission(request.user, 'contact_app.delete_contact')

            actions_html = '<span class="text-muted">No actions</span>'
            if can_edit or can_delete:
                buttons = []
                
                # Read/Unread buttons - FIXED: Use proper URLs
                if can_edit:
                    if contact.is_read:
                        buttons.append(f'''
                            <button type="button" class="btn btn-outline-warning btn-sm mark-unread-btn" 
                               data-contact-id="{contact.id}" data-bs-toggle="tooltip" title="Mark as Unread">
                                <i class="fas fa-envelope"></i>
                            </button>
                        ''')
                    else:
                        buttons.append(f'''
                            <button type="button" class="btn btn-outline-success btn-sm mark-read-btn" 
                               data-contact-id="{contact.id}" data-bs-toggle="tooltip" title="Mark as Read">
                                <i class="fas fa-envelope-open"></i>
                            </button>
                        ''')
                
                # Delete button - FIXED: Use button instead of link with incorrect URL
                if can_delete:
                    buttons.append(f'''
                        <button type="button" class="btn btn-outline-danger btn-sm delete-btn" 
                           data-contact-id="{contact.id}" data-contact-name="{contact.full_name}"
                           data-bs-toggle="tooltip" title="Delete Contact">
                            <i class="fas fa-trash"></i>
                        </button>
                    ''')
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(buttons)}</div>'

            data.append({
                'name': contact.full_name,
                'email': contact.email,
                'phone': phone_html,
                'service': service_html,
                'message': message_html,
                'status': status_html,
                'read_status': read_status_html,
                'is_read': contact.is_read,
                'created_at': contact.created_at.strftime('%Y-%m-%d %H:%M'),
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
        print(f"Error in contact_datatable_api: {str(e)}")
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        }, status=500) 

@rbac_permission_required('contact_app.change_contact')
def contact_mark_read(request):
    """Mark contact as read"""
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.mark_as_read()
            return JsonResponse({'success': True, 'message': 'Contact marked as read'})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Contact not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@rbac_permission_required('contact_app.change_contact')
def contact_mark_unread(request):
    """Mark contact as unread"""
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.mark_as_unread()
            return JsonResponse({'success': True, 'message': 'Contact marked as unread'})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Contact not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})



@rbac_permission_required('contact_app.delete_contact')
def contact_delete(request):
    """Delete contact"""
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        try:
            contact = Contact.objects.get(id=contact_id)
            contact_name = contact.full_name
            contact.delete()
            return JsonResponse({'success': True, 'message': f'Contact {contact_name} deleted successfully'})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Contact not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})