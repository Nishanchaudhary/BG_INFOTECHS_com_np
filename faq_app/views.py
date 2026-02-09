from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import FAQ,Slider
from .forms import FAQForm,SliderForm
from bg_app.decorators import rbac_permission_required

# Helper function to check if user can modify specific FAQ
def can_modify_faq(user, faq):
    """
    Check if user can modify specific FAQ
    - Superusers/staff: always can modify
    - Users with global permission: can modify all FAQs
    - Regular users: can only modify their own FAQs
    """
    if user.is_superuser or user.is_staff:
        return True
    
    # If user has global change permission, they can modify any FAQ
    if user.has_perm('faq_app.change_faq'):
        return True
    
    # Regular users can only modify their own FAQs
    return faq.author == user

# Helper function to get base queryset based on user permissions
def get_faq_queryset(user):
    """
    Return appropriate queryset based on user permissions:
    - Superusers/staff: all FAQs
    - Users with view_faq permission: all FAQs  
    - Regular users: only their own FAQs
    """
    if user.is_superuser or user.is_staff:
        return FAQ.objects.all()
    
    if user.has_perm('faq_app.view_faq'):
        return FAQ.objects.all()
    
    # Regular users without global view permission can only see their own
    return FAQ.objects.filter(author=user)

@rbac_permission_required('faq_app.view_faq')
def faq_list(request):
    """FAQ list view - requires faq_app.view_faq permission"""
    context = {
        'page_title': 'FAQ Management',
        'breadcrumb_active': 'FAQ List',
        'can_add_faq': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.add_faq'),
        'can_change_faq': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.change_faq'),
        'can_delete_faq': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.delete_faq'),
    }
    return render(request, 'faq/faq_list.html', context)

@rbac_permission_required('faq_app.view_faq')
def faqs_datatables(request):
    """Datatables AJAX endpoint - requires faq_app.view_faq permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Get appropriate queryset based on user permissions
        faqs = get_faq_queryset(request.user)
        
        # Total records count
        total_records = faqs.count()
        
        # Search functionality
        if search_value:
            faqs = faqs.filter(
                Q(question__icontains=search_value) |
                Q(answer__icontains=search_value) |
                Q(slug__icontains=search_value) |
                Q(meta_title__icontains=search_value) |
                Q(meta_description__icontains=search_value) |
                Q(author__username__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = faqs.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'question',
            '1': 'slug',
            '2': 'status',
            '3': 'display_order',
            '4': 'author__username',
            '5': 'created_at',
            '6': 'published_at',
        }
        
        order_field = column_map.get(order_column_index, 'display_order')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            faqs = faqs.order_by(order_field)
        else:
            faqs = faqs.order_by('display_order', '-created_at')
        
        # Pagination
        faqs = faqs[start:start + length]
        
        # Prepare data for response
        data = []
        for faq in faqs:
            # Format answer with truncation
            plain_text = strip_tags(faq.answer)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            
            # Answer with clickable tooltip
            answer_html = f'''
                <span class="answer-tooltip" 
                      data-answer="{plain_text}" 
                      data-bs-toggle="tooltip" 
                      title="Click to view full answer">
                    <i class="fas fa-file-alt me-1"></i>
                    {truncated}
                </span>
            '''
            
            # Status badge
            status_badges = {
                'draft': '<span class="badge bg-secondary rounded-pill"><i class="fas fa-edit me-1"></i>Draft</span>',
                'published': '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Published</span>',
                'archived': '<span class="badge bg-warning rounded-pill"><i class="fas fa-archive me-1"></i>Archived</span>'
            }
            status_html = status_badges.get(faq.status, '<span class="badge bg-dark">Unknown</span>')
            
            # Status toggle button - only show if user has change permission for this FAQ
            can_edit_faq = can_modify_faq(request.user, faq)
            status_button = ''
            if can_edit_faq:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm status-toggle-btn {'btn-success' if faq.status == 'published' else 'btn-secondary' if faq.status == 'draft' else 'btn-warning'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas {'fa-check-circle' if faq.status == 'published' else 'fa-edit' if faq.status == 'draft' else 'fa-archive'} me-1"></i>
                            {faq.get_status_display()}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="draft" data-faq-id="{faq.pk}"><i class="fas fa-edit me-2"></i>Draft</a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="published" data-faq-id="{faq.pk}"><i class="fas fa-check-circle me-2"></i>Published</a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="archived" data-faq-id="{faq.pk}"><i class="fas fa-archive me-2"></i>Archived</a></li>
                        </ul>
                    </div>
                '''
            else:
                status_button = status_html
            
            # Format dates
            created_html = faq.created_at.strftime('%Y-%m-%d %H:%M')
            updated_html = faq.updated_at.strftime('%Y-%m-%d %H:%M')
            published_html = faq.published_at.strftime('%Y-%m-%d %H:%M') if faq.published_at else '<span class="text-muted">Not published</span>'
            
            # Display order
            order_html = f'<span class="badge bg-primary"><i class="fas fa-sort-numeric-down me-1"></i>{faq.display_order}</span>'
            
            # Author information
            author_html = f'''
                <span data-bs-toggle="tooltip" title="{faq.author.get_full_name() or faq.author.username}">
                    <i class="fas fa-user me-1"></i>{faq.author.username}
                </span>
            '''
            
            # Actions - only show actions user has permission for
            edit_url = reverse('faq_app:faq_edit', args=[faq.pk])
            delete_url = reverse('faq_app:faq_delete', args=[faq.pk])
            view_url = reverse('faq_app:faq_detail', args=[faq.slug])
            
            # Check permissions for actions
            can_edit = can_modify_faq(request.user, faq)
            can_delete = can_modify_faq(request.user, faq) and (request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.delete_faq'))
            
            actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{view_url}" class="btn btn-outline-primary" target="_blank"
                       data-bs-toggle="tooltip" title="View FAQ (Public Page)">
                        <i class="fas fa-eye"></i>
                    </a>
            '''
            
            if can_edit:
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit FAQ">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            
            if can_delete:
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{faq.question}\\'?')"
                       data-bs-toggle="tooltip" title="Delete FAQ">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            actions_html += '</div>'
            
            # If user has no edit/delete permissions, show message
            if not can_edit and not can_delete:
                actions_html = '<span class="text-muted">View only</span>'
            
            data.append({
                'question': f'<strong>{faq.question}</strong>',
                'slug': f'<code>{faq.slug}</code>',
                'answer': answer_html,
                'status': status_button,
                'display_order': order_html,
                'author': author_html,
                'created_at': f'<i class="fas fa-calendar me-1"></i>{created_html}',
                'updated_at': f'<i class="fas fa-sync me-1"></i>{updated_html}',
                'published_at': published_html,
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
        logger.error(f"Error in faqs_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'An error occurred while processing your request.'
        }, status=500)

@rbac_permission_required('faq_app.add_faq')
def faq_create(request):
    """Create new FAQ - requires faq_app.add_faq permission"""
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.author = request.user
            
            # Set published_at if status is published
            if faq.status == FAQ.Status.PUBLISHED and not faq.published_at:
                faq.published_at = timezone.now()
                
            faq.save()
            messages.success(request, 'FAQ created successfully!')
            return redirect('faq_app:faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FAQForm()
    
    context = {
        'form': form,
        'page_title': 'Create FAQ',
        'breadcrumb_active': 'Create FAQ',
    }
    return render(request, 'faq/faq_form.html', context)

@login_required
def faq_edit(request, pk):
    """Edit existing FAQ"""
    faq = get_object_or_404(FAQ, pk=pk)
    
    # Check if user can edit this specific FAQ using helper function
    if not can_modify_faq(request.user, faq):
        messages.error(request, "You don't have permission to edit this FAQ.")
        return redirect('faq_app:faq_list')
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            updated_faq = form.save(commit=False)
            
            # Update published_at if status changed to published
            if updated_faq.status == FAQ.Status.PUBLISHED and not updated_faq.published_at:
                updated_faq.published_at = timezone.now()
                
            updated_faq.save()
            messages.success(request, 'FAQ updated successfully!')
            return redirect('faq_app:faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FAQForm(instance=faq)
    
    context = {
        'form': form,
        'faq': faq,
        'page_title': f'Edit FAQ - {faq.question}',
        'breadcrumb_active': 'Edit FAQ',
    }
    return render(request, 'faq/faq_form.html', context)

@login_required
def faq_delete(request, pk):
    """Delete FAQ"""
    faq = get_object_or_404(FAQ, pk=pk)
    
    # Check if user can delete this specific FAQ using helper function
    if not can_modify_faq(request.user, faq):
        messages.error(request, "You don't have permission to delete this FAQ.")
        return redirect('faq_app:faq_list')
    
    if request.method == 'POST':
        faq_question = faq.question
        faq.delete()
        messages.success(request, f'FAQ "{faq_question}" deleted successfully!')
        return redirect('faq_app:faq_list')
    
    context = {
        'faq': faq,
        'page_title': 'Delete FAQ',
        'breadcrumb_active': 'Delete FAQ'
    }
    return render(request, 'faq/faq_confirm_delete.html', context)

@login_required
def toggle_faq_status(request, pk):
    """Toggle FAQ status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            faq = get_object_or_404(FAQ, pk=pk)
            
            # Check if user can edit this specific FAQ using helper function
            if not can_modify_faq(request.user, faq):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this FAQ status.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in dict(FAQ.Status.choices):
                faq.status = new_status
                if new_status == 'published' and not faq.published_at:
                    faq.published_at = timezone.now()
                faq.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': faq.status,
                    'status_display': faq.get_status_display(),
                    'message': f'FAQ status updated to {faq.get_status_display()} successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status provided'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def faq_detail(request, slug):
    """Public FAQ detail view - no authentication required"""
    try:
        # Try to get published FAQ
        faq = get_object_or_404(FAQ, slug=slug, status=FAQ.Status.PUBLISHED)
        
        context = {
            'faq': faq,
            'page_title': faq.question,
            'meta_title': faq.meta_title or faq.question,
            'meta_description': faq.meta_description,
        }
        return render(request, 'faq/faq_detail.html', context)
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"FAQ access attempt for slug '{slug}': {str(e)}")
        
        # Check if FAQ exists but is not published
        try:
            faq_exists = FAQ.objects.filter(slug=slug).exists()
            if faq_exists:
                # FAQ exists but not published
                messages.info(request, "This FAQ is not currently available. It may be under review or in draft status.")
                return redirect('faq_app:faq_list')
            else:
                # FAQ doesn't exist at all
                messages.error(request, "The requested FAQ page was not found.")
                return redirect('faq_app:faq_list')
                
        except Exception:
            # Generic error handling
            messages.error(request, "An error occurred while accessing the FAQ page.")
            return redirect('faq_app:faq_list')


# SLIDER VIEW CODE 
# Slider Helper Functions
def can_modify_slider(user, slider):
    """
    Check if user can modify specific slider
    - Superusers/staff: always can modify
    - Users with global permission: can modify all sliders
    - Regular users: can only modify their own sliders
    """
    if user.is_superuser or user.is_staff:
        return True
    
    # If user has global change permission, they can modify any slider
    if user.has_perm('faq_app.change_slider'):
        return True
    
    # Regular users can only modify their own sliders
    return slider.created_by == user

def get_slider_queryset(user):
    """
    Return appropriate queryset based on user permissions:
    - Superusers/staff: all sliders
    - Users with view_slider permission: all sliders  
    - Regular users: only their own sliders
    """
    if user.is_superuser or user.is_staff:
        return Slider.objects.all()
    
    if user.has_perm('faq_app.view_slider'):
        return Slider.objects.all()
    
    # Regular users without global view permission can only see their own
    return Slider.objects.filter(created_by=user)

# Slider Views
@rbac_permission_required('faq_app.view_slider')
def slider_list(request):
    """Slider list view - requires faq_app.view_slider permission"""
    context = {
        'page_title': 'Slider Management',
        'breadcrumb_active': 'Slider List',
        'can_add_slider': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.add_slider'),
        'can_change_slider': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.change_slider'),
        'can_delete_slider': request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.delete_slider'),
    }
    return render(request, 'faq/slider_list.html', context)

@rbac_permission_required('faq_app.view_slider')
def sliders_datatables(request):
    """Datatables AJAX endpoint for sliders - requires faq_app.view_slider permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Get appropriate queryset based on user permissions
        sliders = get_slider_queryset(request.user)
        
        # Total records count
        total_records = sliders.count()
        
        # Search functionality
        if search_value:
            sliders = sliders.filter(
                Q(title__icontains=search_value) |
                Q(short_description__icontains=search_value) |
                Q(link__icontains=search_value) |
                Q(created_by__username__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = sliders.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'title',
            '1': 'status',
            '2': 'order',
            '3': 'created_by__username',
            '4': 'created_at',
            '5': 'start_date',
        }
        
        order_field = column_map.get(order_column_index, 'order')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            sliders = sliders.order_by(order_field)
        else:
            sliders = sliders.order_by('order', '-created_at')
        
        # Pagination
        sliders = sliders[start:start + length]
        
        # Prepare data for response
        data = []
        for slider in sliders:
            # Status badge
            status_badges = {
                'active': '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Active</span>',
                'inactive': '<span class="badge bg-secondary rounded-pill"><i class="fas fa-times-circle me-1"></i>Inactive</span>'
            }
            status_html = status_badges.get(slider.status, '<span class="badge bg-dark">Unknown</span>')
            
            # Current activity status
            current_status = 'Active' if slider.is_currently_active else 'Inactive'
            current_status_badge = 'success' if slider.is_currently_active else 'secondary'
            current_status_html = f'<span class="badge bg-{current_status_badge}"><i class="fas fa-circle me-1"></i>{current_status}</span>'
            
            # Status toggle button - only show if user has change permission for this slider
            can_edit_slider = can_modify_slider(request.user, slider)
            status_button = ''
            if can_edit_slider:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm status-toggle-btn {'btn-success' if slider.status == 'active' else 'btn-secondary'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas {'fa-check-circle' if slider.status == 'active' else 'fa-times-circle'} me-1"></i>
                            {slider.get_status_display()}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="active" data-slider-id="{slider.pk}"><i class="fas fa-check-circle me-2"></i>Active</a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="inactive" data-slider-id="{slider.pk}"><i class="fas fa-times-circle me-2"></i>Inactive</a></li>
                        </ul>
                    </div>
                '''
            else:
                status_button = status_html
            
            # Format dates
            created_html = slider.created_at.strftime('%Y-%m-%d %H:%M')
            updated_html = slider.updated_at.strftime('%Y-%m-%d %H:%M')
            start_html = slider.start_date.strftime('%Y-%m-%d %H:%M') if slider.start_date else '<span class="text-muted">Not set</span>'
            end_html = slider.end_date.strftime('%Y-%m-%d %H:%M') if slider.end_date else '<span class="text-muted">Not set</span>'
            
            # Display order
            order_html = f'<span class="badge bg-primary"><i class="fas fa-sort-numeric-down me-1"></i>{slider.order}</span>'
            
            # Author information
            author_html = f'''
                <span data-bs-toggle="tooltip" title="{slider.created_by.get_full_name() or slider.created_by.username}">
                    <i class="fas fa-user me-1"></i>{slider.created_by.username}
                </span>
            '''
            
            # Image preview
            image_html = f'''
                <img src="{slider.image.url}" alt="{slider.title}" 
                     class="img-thumbnail" style="max-width: 80px; max-height: 60px;"
                     data-bs-toggle="tooltip" title="Click to view full image">
            ''' if slider.image else '<span class="text-muted">No image</span>'
            
            # Link information
            link_html = ''
            if slider.link:
                target = 'target="_blank"' if slider.target_blank else ''
                link_html = f'''
                    <a href="{slider.link}" {target} class="btn btn-sm btn-outline-info" 
                       data-bs-toggle="tooltip" title="{slider.link}">
                        <i class="fas fa-external-link-alt"></i>
                    </a>
                '''
            else:
                link_html = '<span class="text-muted">No link</span>'
            
            # Actions - only show actions user has permission for
            edit_url = reverse('faq_app:slider_edit', args=[slider.pk])
            delete_url = reverse('faq_app:slider_delete', args=[slider.pk])
            view_url = reverse('faq_app:slider_detail', args=[slider.pk])
            
            # Check permissions for actions
            can_edit = can_modify_slider(request.user, slider)
            can_delete = can_modify_slider(request.user, slider) and (request.user.is_superuser or request.user.is_staff or request.user.has_perm('faq_app.delete_slider'))
            
            actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{view_url}" class="btn btn-outline-primary"
                       data-bs-toggle="tooltip" title="View Slider Details">
                        <i class="fas fa-eye"></i>
                    </a>
            '''
            
            if can_edit:
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit Slider">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            
            if can_delete:
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{slider.title}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Slider">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            actions_html += '</div>'
            
            # If user has no edit/delete permissions, show message
            if not can_edit and not can_delete:
                actions_html = '<span class="text-muted">View only</span>'
            
            data.append({
                'title': f'<strong>{slider.title}</strong><br><small class="text-muted">{slider.short_description[:80]}...</small>',
                'image': image_html,
                'status': status_button,
                'current_status': current_status_html,
                'order': order_html,
                'link': link_html,
                'author': author_html,
                'created_at': f'<i class="fas fa-calendar me-1"></i>{created_html}',
                'start_date': start_html,
                'end_date': end_html,
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
        logger.error(f"Error in sliders_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'An error occurred while processing your request.'
        }, status=500)

@rbac_permission_required('faq_app.add_slider')
def slider_create(request):
    """Create new slider - requires faq_app.add_slider permission"""
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            slider = form.save(commit=False)
            slider.created_by = request.user
            slider.save()
            messages.success(request, 'Slider created successfully!')
            return redirect('faq_app:slider_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SliderForm()
    
    context = {
        'form': form,
        'page_title': 'Create Slider',
        'breadcrumb_active': 'Create Slider',
    }
    return render(request, 'faq/slider_form.html', context)

@login_required
def slider_edit(request, pk):
    """Edit existing slider"""
    slider = get_object_or_404(Slider, pk=pk)
    
    # Check if user can edit this specific slider using helper function
    if not can_modify_slider(request.user, slider):
        messages.error(request, "You don't have permission to edit this slider.")
        return redirect('faq_app:slider_list')
    
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully!')
            return redirect('faq_app:slider_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SliderForm(instance=slider)
    
    context = {
        'form': form,
        'slider': slider,
        'page_title': f'Edit Slider - {slider.title}',
        'breadcrumb_active': 'Edit Slider',
    }
    return render(request, 'faq/slider_form.html', context)

@login_required
def slider_delete(request, pk):
    """Delete slider"""
    slider = get_object_or_404(Slider, pk=pk)
    
    # Check if user can delete this specific slider using helper function
    if not can_modify_slider(request.user, slider):
        messages.error(request, "You don't have permission to delete this slider.")
        return redirect('faq_app:slider_list')
    
    if request.method == 'POST':
        slider_title = slider.title
        slider.delete()
        messages.success(request, f'Slider "{slider_title}" deleted successfully!')
        return redirect('faq_app:slider_list')
    
    context = {
        'slider': slider,
        'page_title': 'Delete Slider',
        'breadcrumb_active': 'Delete Slider'
    }
    return render(request, 'faq/slider_confirm_delete.html', context)

@login_required
def toggle_slider_status(request, pk):
    """Toggle slider status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            slider = get_object_or_404(Slider, pk=pk)
            
            # Check if user can edit this specific slider using helper function
            if not can_modify_slider(request.user, slider):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this slider status.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in dict(Slider.Status.choices):
                slider.status = new_status
                slider.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': slider.status,
                    'status_display': slider.get_status_display(),
                    'is_currently_active': slider.is_currently_active,
                    'message': f'Slider status updated to {slider.get_status_display()} successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status provided'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def slider_detail(request, pk):
    """Slider detail view"""
    slider = get_object_or_404(Slider, pk=pk)
    
    context = {
        'slider': slider,
        'page_title': slider.title,
    }
    return render(request, 'faq/slider_detail.html', context)

def active_sliders(request):
    """Get active sliders for public display"""
    sliders = Slider.objects.get_ordered_active()
    
    # Filter by date range if needed
    current_sliders = [s for s in sliders if s.is_currently_active]
    
    return JsonResponse({
        'sliders': [
            {
                'title': s.title,
                'description': s.short_description,
                'image_url': s.image.url if s.image else None,
                'link': s.link,
                'target_blank': s.target_blank,
                'order': s.order
            }
            for s in current_sliders
        ]
    })