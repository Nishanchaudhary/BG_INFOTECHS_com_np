from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import Vacancy,JobType ,JobApplication
from .forms import VacancyForm,JobApplicationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Import RBAC decorators
from bg_app.decorators import rbac_permission_required

# Helper function to check if user can modify specific vacancy
def can_modify_vacancy(user, vacancy):
    """
    Check if user can modify specific vacancy 
    - Superuser/staff: always can modify
    - Users with global permission: can modify all vacancies
    - Regular users: can only modify their own vacancies
    """
    if user.is_superuser or user.is_staff:
        return True
    
    # If user has global change permission, they can modify any vacancy
    if user.has_perm('vacancy_app.change_vacancy'):
        return True
    
    # Regular users can only modify their own vacancies
    return vacancy.author == user

# Helper function to get base queryset based on user permissions
def get_vacancy_queryset(user):
    """
    Return appropriate queryset based on user permissions:
    - Superusers/staff: all vacancies
    - Users with view_vacancy permission: all vacancies  
    - Regular users: only their own vacancies
    """
    if user.is_superuser or user.is_staff:
        return Vacancy.objects.all()
    
    if user.has_perm('vacancy_app.view_vacancy'):
        return Vacancy.objects.all()
    
    # Regular users without global view permission can only see their own
    return Vacancy.objects.filter(author=user)



@rbac_permission_required('vacancy_app.view_vacancy')
def vacancy_list(request):
    """Vacancy list view - requires view_vacancy permission"""
    vacancy_filter = request.GET.get('vacancy', '')

    context = {
        'page_title': 'Vacancy Management',
        'breadcrumb_active': 'Vacancy List',
        'vacancy_filter': vacancy_filter,
        'can_add_vacancy': request.user.is_superuser or request.user.is_staff or request.user.has_perm('vacancy_app.add_vacancy'),
        'can_change_vacancy': request.user.is_superuser or request.user.is_staff or request.user.has_perm('vacancy_app.change_vacancy'),
        'can_delete_vacancy': request.user.is_superuser or request.user.is_staff or request.user.has_perm('vacancy_app.delete_vacancy'),
    }
    return render(request, 'vacancy/vacancy_list.html', context)

@rbac_permission_required('vacancy_app.view_vacancy')
def vacancies_datatables(request):
    """Datatables AJAX endpoint - requires view_vacancy permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Get appropriate queryset based on user permissions
        vacancies = get_vacancy_queryset(request.user)
        
        # Total records count
        total_records = vacancies.count()
        
        # Search functionality
        if search_value:
            search_filter = Q()
            
            # Add search conditions for each field individually
            if search_value:
                search_filter |= Q(title__icontains=search_value)
                search_filter |= Q(short_description__icontains=search_value)
                search_filter |= Q(address__icontains=search_value)
                search_filter |= Q(author__username__icontains=search_value)
                search_filter |= Q(skills__icontains=search_value)
                search_filter |= Q(status__icontains=search_value)
                search_filter |= Q(job_type__icontains=search_value)
            
            vacancies = vacancies.filter(search_filter)
        
        # Filtered records count
        filtered_records = vacancies.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'title',
            '1': 'job_type',
            '2': 'address', 
            '3': 'salary',
            '4': 'status',
            '5': 'expired_date',
            '6': 'author__username',
            '7': 'created_at',
            '8': 'updated_at',
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            vacancies = vacancies.order_by(order_field)
        else:
            vacancies = vacancies.order_by('-created_at')
        
        # Pagination
        vacancies = vacancies[start:start + length]
        
        # Prepare data for response
        data = []
        for vacancy in vacancies:
            # Format description with truncation
            plain_text = strip_tags(vacancy.description)
            truncated = plain_text[:80] + "..." if len(plain_text) > 80 else plain_text
            
            # Description with clickable tooltip
            description_html = f'''
                <span class="description-tooltip" 
                      data-description="{plain_text}" 
                      data-bs-toggle="tooltip" 
                      title="Click to view full description">
                    <i class="fas fa-file-alt me-1"></i>
                    {truncated}
                </span>
            '''
            
            # Job type badge
            job_type_badges = {
                'full_time': '<span class="badge bg-primary rounded-pill"><i class="fas fa-briefcase me-1"></i>Full Time</span>',
                'part_time': '<span class="badge bg-info rounded-pill"><i class="fas fa-clock me-1"></i>Part Time</span>',
                'hybrid': '<span class="badge bg-warning rounded-pill"><i class="fas fa-balance-scale me-1"></i>Hybrid</span>',
                'remote': '<span class="badge bg-success rounded-pill"><i class="fas fa-home me-1"></i>Remote</span>'
            }
            job_type_html = job_type_badges.get(vacancy.job_type, '<span class="badge bg-dark">Unknown</span>')
            
            # Status badge with enhanced styling
            status_badges = {
                'active': '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Active</span>',
                'inactive': '<span class="badge bg-secondary rounded-pill"><i class="fas fa-pause-circle me-1"></i>Inactive</span>',
                'draft': '<span class="badge bg-warning rounded-pill"><i class="fas fa-edit me-1"></i>Draft</span>'
            }
            status_html = status_badges.get(vacancy.status, '<span class="badge bg-dark">Unknown</span>')
            
            # Enhanced Status toggle with real-time editing
            can_edit_this_vacancy = can_modify_vacancy(request.user, vacancy)
            status_button = ''
            
            if can_edit_this_vacancy:
                # Enhanced status dropdown with better UX
                status_button = f'''
                    <div class="dropdown status-dropdown">
                        <button class="btn btn-sm status-toggle-btn {'btn-success' if vacancy.status == 'active' else 'btn-secondary' if vacancy.status == 'inactive' else 'btn-warning'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" 
                                data-vacancy-id="{vacancy.pk}"
                                data-current-status="{vacancy.status}"
                                aria-expanded="false">
                            <i class="fas {'fa-check-circle' if vacancy.status == 'active' else 'fa-pause-circle' if vacancy.status == 'inactive' else 'fa-edit'} me-1"></i>
                            {vacancy.status.title()}
                        </button>
                        <ul class="dropdown-menu status-dropdown-menu">
                            <li>
                                <a class="dropdown-item status-change-option {'active' if vacancy.status == 'active' else ''}" 
                                   href="#" 
                                   data-status="active" 
                                   data-vacancy-id="{vacancy.pk}">
                                    <i class="fas fa-check-circle text-success me-2"></i>Active
                                    {'<i class="fas fa-check float-end mt-1"></i>' if vacancy.status == 'active' else ''}
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item status-change-option {'active' if vacancy.status == 'inactive' else ''}" 
                                   href="#" 
                                   data-status="inactive" 
                                   data-vacancy-id="{vacancy.pk}">
                                    <i class="fas fa-pause-circle text-secondary me-2"></i>Inactive
                                    {'<i class="fas fa-check float-end mt-1"></i>' if vacancy.status == 'inactive' else ''}
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item status-change-option {'active' if vacancy.status == 'draft' else ''}" 
                                   href="#" 
                                   data-status="draft" 
                                   data-vacancy-id="{vacancy.pk}">
                                    <i class="fas fa-edit text-warning me-2"></i>Draft
                                    {'<i class="fas fa-check float-end mt-1"></i>' if vacancy.status == 'draft' else ''}
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-info status-history-btn" 
                                   href="#" 
                                   data-vacancy-id="{vacancy.pk}"
                                   data-bs-toggle="modal" 
                                   data-bs-target="#statusHistoryModal">
                                    <i class="fas fa-history me-2"></i>View Status History
                                </a>
                            </li>
                        </ul>
                    </div>
                '''
            else:
                # Read-only status display for users without edit permissions
                status_button = f'''
                    <span class="badge {'bg-success' if vacancy.status == 'active' else 'bg-secondary' if vacancy.status == 'inactive' else 'bg-warning'} rounded-pill">
                        <i class="fas {'fa-check-circle' if vacancy.status == 'active' else 'fa-pause-circle' if vacancy.status == 'inactive' else 'fa-edit'} me-1"></i>
                        {vacancy.status.title()}
                    </span>
                '''
            
            # Format dates
            created_html = vacancy.created_at.strftime('%Y-%m-%d %H:%M')
            updated_html = vacancy.updated_at.strftime('%Y-%m-%d %H:%M')
            expired_html = vacancy.expired_date.strftime('%Y-%m-%d')
            
            # Enhanced expired status with auto-detection
            is_expired = vacancy.is_expired()
            expired_badge = '''
                <span class="badge bg-danger" data-bs-toggle="tooltip" title="This vacancy has expired">
                    <i class="fas fa-exclamation-triangle me-1"></i>Expired
                </span>
            ''' if is_expired else '''
                <span class="badge bg-success" data-bs-toggle="tooltip" title="Active vacancy">
                    <i class="fas fa-check me-1"></i>Active
                </span>
            '''
            
            # Auto-disable status editing for expired vacancies
            if is_expired and can_edit_this_vacancy:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm status-toggle-btn btn-danger disabled"
                                type="button"
                                data-bs-toggle="tooltip" 
                                title="Cannot change status - vacancy has expired">
                            <i class="fas fa-ban me-1"></i>
                            Expired
                        </button>
                    </div>
                '''
            
            # Salary format
            try:
                salary_value = int(vacancy.salary)
                salary_html = f'<span class="badge bg-primary"><i class="fas fa-money-bill-wave me-1"></i>{salary_value:,}</span>'
            except (ValueError, TypeError):
                salary_html = f'<span class="badge bg-primary"><i class="fas fa-money-bill-wave me-1"></i>{vacancy.salary}</span>'
            
            # Skills with tooltip
            skills_list = vacancy.get_skills_list()
            if skills_list:
                skills_display = skills_list[0] + "..." if len(skills_list) > 1 else skills_list[0]
            else:
                skills_display = "No skills"
                
            skills_html = f'''
                <span class="skills-tooltip" 
                      data-skills="{', '.join(skills_list) if skills_list else 'No skills specified'}" 
                      data-bs-toggle="tooltip" 
                      title="Click to view all skills">
                    <i class="fas fa-tools me-1"></i>
                    {skills_display}
                </span>
            '''
            
            # Actions with enhanced permissions check
            edit_url = reverse('vacancy_app:vacancy_edit', args=[vacancy.pk])
            delete_url = reverse('vacancy_app:vacancy_delete', args=[vacancy.pk])
            view_url = reverse('vacancy_app:vacancy_detail', args=[vacancy.pk])
            
            # Check permissions for actions
            can_view = request.user.is_superuser or request.user.is_staff or request.user.has_perm('vacancy_app.view_vacancy') or vacancy.author == request.user
            can_edit = can_modify_vacancy(request.user, vacancy)
            can_delete = can_modify_vacancy(request.user, vacancy) and (request.user.is_superuser or request.user.is_staff or request.user.has_perm('vacancy_app.delete_vacancy'))
            
            actions_html = '<div class="btn-group btn-group-sm" role="group">'
            
            if can_view:
                actions_html += f'''
                    <a href="{view_url}" class="btn btn-outline-primary" target="_blank"
                       data-bs-toggle="tooltip" title="View Vacancy Details">
                        <i class="fas fa-eye"></i>
                    </a>
                '''
            
            if can_edit:
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit Vacancy">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            
            # Quick status actions for super users and staff
            if can_edit and request.user.is_superuser:
                actions_html += f'''
                    <button class="btn btn-outline-info quick-activate-btn" 
                            data-vacancy-id="{vacancy.pk}"
                            data-bs-toggle="tooltip" 
                            title="Quick Activate">
                        <i class="fas fa-bolt"></i>
                    </button>
                '''
            
            if can_delete:
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{vacancy.title}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Vacancy">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            actions_html += '</div>'
            
            # Add status indicator for quick scanning
            status_indicator = f'''
                <div class="status-indicator {'status-active' if vacancy.status == 'active' else 'status-inactive' if vacancy.status == 'inactive' else 'status-draft'}"
                     data-bs-toggle="tooltip" 
                     title="Status: {vacancy.status.title()}">
                </div>
            '''
            
            data.append({
                'title': f'<strong>{vacancy.title}</strong>{status_indicator}',
                'job_type': job_type_html,
                'address': f'<i class="fas fa-map-marker-alt me-1"></i> {vacancy.address}',
                'description': description_html,
                'skills': skills_html,
                'salary': salary_html,
                'status': status_button,
                'expired_date': f'{expired_html} {expired_badge}',
                'author': vacancy.author.username,
                'created_at': f'<i class="fas fa-calendar me-1"></i>{created_html}',
                'updated_at': f'<i class="fas fa-sync me-1"></i>{updated_html}',
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
        logger.error(f"Error in vacancies_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'An error occurred while processing your request.'
        }, status=500)

# Add this new view for handling status updates via AJAX
@rbac_permission_required('vacancy_app.change_vacancy')
def update_vacancy_status(request):
    """Update vacancy status via AJAX - requires change_vacancy permission"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            vacancy_id = request.POST.get('vacancy_id')
            new_status = request.POST.get('status')
            
            if not vacancy_id or not new_status:
                return JsonResponse({
                    'success': False,
                    'message': 'Vacancy ID and status are required.'
                }, status=400)
            
            # Get the vacancy
            vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
            
            # Check if user can modify this vacancy
            if not can_modify_vacancy(request.user, vacancy):
                return JsonResponse({
                    'success': False,
                    'message': 'You do not have permission to modify this vacancy.'
                }, status=403)
            
            # Validate status
            valid_statuses = ['active', 'inactive', 'draft']
            if new_status not in valid_statuses:
                return JsonResponse({
                    'success': False,
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }, status=400)
            
            # Check if vacancy is expired
            if vacancy.is_expired() and new_status != 'inactive':
                return JsonResponse({
                    'success': False,
                    'message': 'Cannot change status of expired vacancy. Only inactive status is allowed.'
                }, status=400)
            
            # Update status
            old_status = vacancy.status
            vacancy.status = new_status
            vacancy.updated_by = request.user
            vacancy.save()
            
            # Log status change (you might want to create a StatusHistory model)
            # StatusHistory.objects.create(
            #     vacancy=vacancy,
            #     old_status=old_status,
            #     new_status=new_status,
            #     changed_by=request.user
            # )
            
            return JsonResponse({
                'success': True,
                'message': f'Status updated successfully from {old_status} to {new_status}.',
                'new_status': new_status,
                'vacancy_id': vacancy_id
            })
            
        except Vacancy.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Vacancy not found.'
            }, status=404)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error updating vacancy status: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while updating the status.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

@rbac_permission_required('vacancy_app.add_vacancy')
def vacancy_create(request):
    """Create new vacancy - requires add_vacancy permission"""
    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.author = request.user
            vacancy.save()
            messages.success(request, 'Vacancy created successfully!')
            return redirect('vacancy_app:vacancy_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VacancyForm()
    
    context = {
        'form': form,
        'page_title': 'Create Vacancy',
        'breadcrumb_active': 'Create Vacancy',
        'breadcrumb_icon': 'plus'
    }
    return render(request, 'vacancy/vacancy_form.html', context)

@login_required
def vacancy_edit(request, pk):
    """Edit existing vacancy - requires change_vacancy permission"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    
    # Check change permission using helper function
    if not can_modify_vacancy(request.user, vacancy):
        messages.error(request, "You don't have permission to edit this vacancy.")
        return redirect('vacancy_app:vacancy_list')
    
    if request.method == 'POST':
        form = VacancyForm(request.POST, request.FILES, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vacancy updated successfully!')
            return redirect('vacancy_app:vacancy_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VacancyForm(instance=vacancy)
    
    context = {
        'form': form,
        'vacancy': vacancy,
        'page_title': f'Edit Vacancy - {vacancy.title}',
        'breadcrumb_active': 'Edit Vacancy',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'vacancy/vacancy_form.html', context)

@login_required
def vacancy_delete(request, pk):
    """Delete vacancy - requires delete_vacancy permission"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    
    # Check delete permission using helper function
    if not can_modify_vacancy(request.user, vacancy):
        messages.error(request, "You don't have permission to delete this vacancy.")
        return redirect('vacancy_app:vacancy_list')
    
    if request.method == 'POST':
        vacancy_title = vacancy.title
        vacancy.delete()
        messages.success(request, f'Vacancy "{vacancy_title}" deleted successfully!')
        return redirect('vacancy_app:vacancy_list')
    
    context = {
        'vacancy': vacancy,
        'page_title': 'Delete Vacancy',
        'breadcrumb_active': 'Delete Vacancy'
    }
    return render(request, 'vacancy/vacancy_confirm_delete.html', context)

@login_required
def toggle_vacancy_status(request, pk):
    """Toggle vacancy status via AJAX - requires change_vacancy permission"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            vacancy = get_object_or_404(Vacancy, pk=pk)
            
            # Check change permission using helper function
            if not can_modify_vacancy(request.user, vacancy):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change the status of this vacancy.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in dict(Vacancy.Status.choices):
                vacancy.status = new_status
                vacancy.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': vacancy.status,
                    'new_status_display': vacancy.get_status_display(),
                    'message': f'Vacancy status updated to {vacancy.get_status_display()} successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status provided'
                }, status=400)
                
        except Vacancy.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Vacancy not found'
            }, status=404)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in toggle_vacancy_status: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'An internal server error occurred'
            }, status=500)
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method or not AJAX'
    }, status=400)

def vacancy_detail(request, pk):
    """Public vacancy detail view - no authentication required"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    
    # Check if vacancy is active and not expired for public view
    if vacancy.status != 'active' or vacancy.is_expired():
        messages.warning(request, "This vacancy is no longer available.")
    
    context = {
        'vacancy': vacancy,
        'page_title': vacancy.title
    }
    return render(request, 'vacancy/vacancy_detail.html', context)



# Job Application Views
# Helper functions for JobApplication - Updated for Django permissions only
def can_modify_application(user, application):
    """
    Check if user can modify specific job application using Django permissions only
    - Superusers: always can modify
    - Users with global permission: can modify all applications  
    - Regular users: can only modify applications for vacancies they created
    """
    if user.is_superuser:
        return True
    
    # If user has global change permission, they can modify any application
    if user.has_perm('teams_app.change_jobapplication'):
        return True
    
    # Regular users can only modify applications for vacancies they created
    return application.vacancy.author == user

def get_applications_queryset(user):
    """
    Return appropriate queryset based on user permissions (Django permissions only):
    - Superusers: all applications
    - Users with view_jobapplication permission: all applications  
    - Regular users: only applications for vacancies they created
    """
    if user.is_superuser:
        return JobApplication.objects.all()
    
    if user.has_perm('teams_app.view_jobapplication'):
        return JobApplication.objects.all()
    
    # Regular users without global view permission can only see applications for their vacancies
    return JobApplication.objects.filter(vacancy__author=user)





@rbac_permission_required('vacancy_app.view_jobapplication')
def application_list(request):
    """Job application list view"""
    vacancy_filter = request.GET.get('vacancy', '')

    context = {
        'page_title': 'Job Applications',
        'breadcrumb_active': 'Application List',
        'vacancy_filter': vacancy_filter,
        'can_change_application': request.user.has_perm('vacancy_app.change_jobapplication'),
        'can_delete_application': request.user.has_perm('vacancy_app.delete_jobapplication'),
    }
    return render(request, 'vacancy/application_list.html', context)

@rbac_permission_required('vacancy_app.view_jobapplication')
def application_datatables(request):
    """Datatables AJAX endpoint for job applications"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        vacancy_filter = request.GET.get('vacancy', '')
    
        # Get appropriate queryset based on user permissions
        applications = get_applications_queryset(request.user)
        
        # Apply vacancy filter if provided
        if vacancy_filter:
            applications = applications.filter(vacancy_id=vacancy_filter)
        
        # Total records count
        total_records = applications.count()
        
        # Search functionality
        if search_value:
            applications = applications.filter(
                Q(full_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                Q(vacancy__title__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = applications.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'full_name',
            '1': 'vacancy__title', 
            '2': 'email',
            '3': 'status',
            '4': 'applied_at',
        }
        
        order_field = column_map.get(order_column_index, 'applied_at')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            applications = applications.order_by(order_field)
        else:
            applications = applications.order_by('-applied_at')
        
        # Pagination
        applications = applications[start:start + length]
        
        # Prepare data for response
        data = []
        for application in applications:
            # Format cover letter with truncation
            plain_text = strip_tags(application.cover_letter)
            truncated = plain_text[:60] + "..." if len(plain_text) > 60 else plain_text
            cover_letter_html = f'''
                <span class="description-tooltip" 
                      data-description="{plain_text}" 
                      data-bs-toggle="tooltip" 
                      title="Click to view full cover letter">
                    <i class="fas fa-file-alt me-1"></i>
                    {truncated}
                </span>
            '''
            
            # Status display with enhanced editing features
            status_colors = {
                'pending': 'warning',
                'reviewed': 'info',
                'accepted': 'success', 
                'rejected': 'danger'
            }
            status_color = status_colors.get(application.status, 'secondary')
            
            # Enhanced Status dropdown with real-time editing
            can_change_application = can_modify_application(request.user, application)
            status_button = ''
            
            # Define icons for each status
            status_icons = {
                'pending': 'fa-clock',
                'reviewed': 'fa-eye',
                'accepted': 'fa-check',
                'rejected': 'fa-times'
            }
            
            current_icon = status_icons.get(application.status, 'fa-question')
            
            if can_change_application:
                # Enhanced status dropdown with better UX
                status_button = f'''
                    <div class="dropdown status-dropdown">
                        <button class="btn btn-sm status-badge status-{application.status} status-editable dropdown-toggle status-dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" 
                                data-application-id="{application.pk}"
                                data-current-status="{application.status}"
                                aria-expanded="false">
                            <i class="fas {current_icon} me-1"></i>
                            {application.get_status_display()}
                        </button>
                        <ul class="dropdown-menu status-dropdown-menu">
                            <li>
                                <a class="dropdown-item status-dropdown-item {'active' if application.status == 'pending' else ''}" 
                                   href="#" 
                                   data-status="pending" 
                                   data-application-id="{application.pk}">
                                    <i class="fas fa-clock text-warning me-2"></i>Pending
                                    {'<i class="fas fa-check float-end mt-1"></i>' if application.status == 'pending' else ''}
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item status-dropdown-item {'active' if application.status == 'reviewed' else ''}" 
                                   href="#" 
                                   data-status="reviewed" 
                                   data-application-id="{application.pk}">
                                    <i class="fas fa-eye text-info me-2"></i>Reviewed
                                    {'<i class="fas fa-check float-end mt-1"></i>' if application.status == 'reviewed' else ''}
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item status-dropdown-item {'active' if application.status == 'accepted' else ''}" 
                                   href="#" 
                                   data-status="accepted" 
                                   data-application-id="{application.pk}">
                                    <i class="fas fa-check text-success me-2"></i>Accepted
                                    {'<i class="fas fa-check float-end mt-1"></i>' if application.status == 'accepted' else ''}
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item status-dropdown-item {'active' if application.status == 'rejected' else ''}" 
                                   href="#" 
                                   data-status="rejected" 
                                   data-application-id="{application.pk}">
                                    <i class="fas fa-times text-danger me-2"></i>Rejected
                                    {'<i class="fas fa-check float-end mt-1"></i>' if application.status == 'rejected' else ''}
                                </a>
                            </li>
                        </ul>
                    </div>
                '''
            else:
                # Read-only status display for users without edit permissions
                status_button = f'''
                    <span class="status-badge status-{application.status}">
                        <i class="fas {current_icon} me-1"></i>
                        {application.get_status_display()}
                    </span>
                '''
            
            # Resume download link
            if application.resume:
                resume_html = f'''
                    <a href="{application.resume.url}" target="_blank" class="btn btn-sm btn-outline-primary" 
                       data-bs-toggle="tooltip" title="Download Resume">
                        <i class="fas fa-download me-1"></i>Resume
                    </a>
                '''
            else:
                resume_html = '<span class="text-muted">No resume</span>'
            
            # Format dates
            applied_html = application.applied_at.strftime('%Y-%m-%d %H:%M')
            
            actions_html = '<div class="btn-group btn-group-sm" role="group">'
            
            # Check delete permission
            if can_modify_application(request.user, application):
                delete_url = reverse('vacancy_app:application_delete', args=[application.pk])
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete this application from \\'{application.full_name}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Application">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            # Check edit permission  
            if can_modify_application(request.user, application):
                edit_url = reverse('vacancy_app:application_edit', args=[application.pk])
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" data-bs-toggle="tooltip" title="Edit Application">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            else:
                actions_html += '''
                    <span class="btn btn-outline-secondary disabled" data-bs-toggle="tooltip" title="No permissions">
                        <i class="fas fa-ban"></i>
                    </span>
                '''
            
            actions_html += '</div>'
            
            data.append({
                'full_name': f'<strong>{application.full_name}</strong>',
                'vacancy': f'<a href="{reverse("vacancy_app:vacancy_list")}" class="text-decoration-none">{application.vacancy.title}</a>',
                'email': f'<a href="mailto:{application.email}">{application.email}</a>',
                'phone': application.phone,
                'cover_letter': cover_letter_html,
                'resume': resume_html,
                'status': status_button,
                'applied_at': f'<small>{applied_html}</small>',
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
        logger.error(f"Error in application_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'Server error occurred'
        }, status=500)


# @require_POST
# @csrf_exempt
# def update_application_status(request):
#     """Update application status via AJAX"""
#     try:
#         application_id = request.POST.get('application_id')
#         new_status = request.POST.get('status')
        
#         if not application_id or not new_status:
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Application ID and status are required.'
#             }, status=400)
        
#         # Get the application
#         application = get_object_or_404(JobApplication, pk=application_id)
        
#         # Check permissions using the helper function
#         if not can_modify_application(request.user, application):
#             return JsonResponse({
#                 'success': False,
#                 'error': 'You do not have permission to change application status.'
#             }, status=403)
        
#         # Validate status
#         valid_statuses = ['pending', 'reviewed', 'accepted', 'rejected']
#         if new_status not in valid_statuses:
#             return JsonResponse({
#                 'success': False,
#                 'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
#             }, status=400)
        
#         # Update status
#         old_status = application.status
#         application.status = new_status
#         application.save()
        
#         # Return success response
#         status_display = dict(JobApplication.ApplicationStatus.choices).get(new_status, new_status)
        
#         return JsonResponse({
#             'success': True,
#             'message': f'Status updated successfully from {old_status} to {new_status}.',
#             'new_status': new_status,
#             'new_status_display': status_display.title(),
#             'application_id': application_id
#         })
        
#     except JobApplication.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'error': 'Application not found.'
#         }, status=404)
#     except Exception as e:
#         import logging
#         logger = logging.getLogger(__name__)
#         logger.error(f"Error updating application status: {str(e)}")
#         return JsonResponse({
#             'success': False,
#             'error': 'An error occurred while updating the status.'
#         }, status=500)

    
def application_create(request, vacancy_pk=None):
    """Create new job application (public facing) - No permission required for public access"""
    vacancy = None
    if vacancy_pk:
        vacancy = get_object_or_404(Vacancy, pk=vacancy_pk, status='active')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                if vacancy:
                    application.vacancy = vacancy
                application.save()
                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('vacancy_app:application_list')
            
            except Exception as e:
                messages.error(request, 'You have already applied for this position.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if vacancy:
            initial['vacancy'] = vacancy
        form = JobApplicationForm(initial=initial)
    
    # Get active vacancies for dropdown
    active_vacancies = Vacancy.objects.filter(status='active')
    
    context = {
        'form': form,
        'vacancy': vacancy,
        'active_vacancies': active_vacancies,
        'page_title': 'Apply for Position',
    }
    return render(request, 'vacancy/application_form.html', context)

def application_edit(request, pk):
    """Edit job application - requires change permission"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    # Check change permission using helper function
    if not can_modify_application(request.user, application):
        messages.error(request, "You don't have permission to edit this application.")
        return redirect('vacancy_app:application_list')
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully!')
            return redirect('vacancy_app:application_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm(instance=application)
    
    context = {
        'form': form,
        'application': application,
        'page_title': f'Edit Application - {application.full_name}',
        'breadcrumb_active': 'Edit Application',
        'breadcrumb_icon': 'edit'
    }
    return render(request, 'vacancy/application_form.html', context)


@rbac_permission_required('vacancy_app.delete_jobapplication')
def application_delete(request, pk):
    """Delete job application - requires delete permission"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    
    if request.method == 'POST':
        applicant_name = application.full_name
        application.delete()
        messages.success(request, f'Application from "{applicant_name}" deleted successfully!')
        return redirect('vacancy_app:application_list')
    
    context = {
        'application': application,
        'page_title': 'Delete Application',
        'breadcrumb_active': 'Delete Application'
    }
    return render(request, 'vacancy/application_confirm_delete.html', context)


@require_POST
@csrf_exempt
def toggle_application_status(request, pk):
    """Update application status via AJAX - Fixed version"""
    try:
        application_id = pk
        new_status = request.POST.get('status')
        
        if not new_status:
            return JsonResponse({
                'success': False,
                'error': 'Status is required.'
            }, status=400)
        
        # Get the application
        application = get_object_or_404(JobApplication, pk=application_id)
        
        # Check permissions using the helper function
        if not can_modify_application(request.user, application):
            return JsonResponse({
                'success': False,
                'error': 'You do not have permission to change application status.'
            }, status=403)
        
        # Validate status
        valid_statuses = ['pending', 'reviewed', 'accepted', 'rejected']
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }, status=400)
        
        # Update status
        old_status = application.status
        application.status = new_status
        application.save()
        
        # Return success response
        status_display = dict(JobApplication.ApplicationStatus.choices).get(new_status, new_status)
        
        return JsonResponse({
            'success': True,
            'message': f'Status updated successfully from {old_status} to {new_status}.',
            'new_status': new_status,
            'new_status_display': status_display,
            'application_id': application_id
        })
        
    except JobApplication.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Application not found.'
        }, status=404)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating application status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while updating the status.'
        }, status=500)
