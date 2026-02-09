from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from .models import Teams
from .forms import TeamsForm
from bg_app.decorators import rbac_permission_required

# Helper function to check if user can modify specific team member
def can_modify_team(user, team):
    """
    Check if user can modify specific team member 
    - Superusers/staff: always can modify
    - Users with global permission: can modify all teams
    - Regular users: can only modify their own teams
    """
    if user.is_superuser or user.is_staff:
        return True
    
    # If user has global change permission, they can modify any team
    if user.has_perm('teams_app.change_teams'):
        return True
    
    # Regular users can only modify their own teams
    return team.author == user

# Helper function to get base queryset based on user permissions
def get_teams_queryset(user):
    """
    Return appropriate queryset based on user permissions:
    - Superusers/staff: all teams
    - Users with view_teams permission: all teams  
    - Regular users: only their own teams
    """
    if user.is_superuser or user.is_staff:
        return Teams.objects.all()
    
    if user.has_perm('teams_app.view_teams'):
        return Teams.objects.all()
    
    # Regular users without global view permission can only see their own
    return Teams.objects.filter(author=user)

@rbac_permission_required('teams_app.view_teams')
def teams_list(request):
    """Teams list view - requires teams_app.view_teams permission"""
    context = {
        'page_title': 'Team Management',
        'breadcrumb_active': 'Team List',
        'can_create_team': request.user.is_superuser or request.user.is_staff or request.user.has_perm('teams_app.add_teams'),
    }
    return render(request, 'teams/teams_list.html', context)

@rbac_permission_required('teams_app.view_teams')
def teams_datatables(request):
    """Datatables AJAX endpoint - requires teams_app.view_teams permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Get appropriate queryset based on user permissions
        teams = get_teams_queryset(request.user)
        
        # Total records count
        total_records = teams.count()
        
        # Search functionality
        if search_value:
            teams = teams.filter(
                Q(name__icontains=search_value) |
                Q(designation__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                Q(skills__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(author__username__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = teams.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'name',
            '1': 'designation', 
            '2': 'email',
            '3': 'status',
            '4': 'display_order',
            '5': 'author__username',
            '6': 'created_at',
        }
        
        order_field = column_map.get(order_column_index, 'display_order')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            teams = teams.order_by(order_field)
        else:
            teams = teams.order_by('display_order', '-created_at')
        
        # Pagination
        teams = teams[start:start + length]
        
        # Prepare data for response
        data = []
        for team in teams:
            # Format description with truncation
            plain_text = strip_tags(team.description)
            truncated = plain_text[:60] + "..." if len(plain_text) > 60 else plain_text
            
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
            
            # Skills display
            skills_list = team.get_skills_list()[:3]
            skills_html = ''
            for skill in skills_list:
                skills_html += f'<span class="badge bg-info me-1 mb-1">{skill}</span>'
            if len(team.get_skills_list()) > 3:
                skills_html += f'<span class="badge bg-secondary">+{len(team.get_skills_list()) - 3} more</span>'
            
            # Status display
            if team.status == 'active':
                status_html = '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Active</span>'
            else:
                status_html = '<span class="badge bg-danger rounded-pill"><i class="fas fa-times-circle me-1"></i>Inactive</span>'
            
            # Status toggle button - only if user has change permission for this team
            can_change_team = can_modify_team(request.user, team)
            
            status_button = ''
            if can_change_team:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm {'btn-success' if team.status == 'active' else 'btn-danger'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas {'fa-check-circle' if team.status == 'active' else 'fa-times-circle'} me-1"></i>
                            {team.status.title()}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="active" data-team-id="{team.pk}">
                                <i class="fas fa-check-circle me-2 text-success"></i>Active
                            </a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="inactive" data-team-id="{team.pk}">
                                <i class="fas fa-times-circle me-2 text-danger"></i>Inactive
                            </a></li>
                        </ul>
                    </div>
                '''
            else:
                status_button = status_html
            
            # Image display
            if team.image:
                image_html = f'<img src="{team.image.url}" alt="{team.name}" class="rounded-circle" width="45" height="45" style="object-fit: cover;">'
            else:
                image_html = '''
                    <div class="rounded-circle d-flex align-items-center justify-content-center bg-light border" 
                         style="width: 45px; height: 45px;">
                        <i class="fas fa-user text-muted"></i>
                    </div>
                '''
            
            # Social links
            social_html = ''
            social_platforms = [
                ('facebook', 'fab fa-facebook text-primary'),
                ('twitter', 'fab fa-twitter text-info'),
                ('linkedin', 'fab fa-linkedin text-primary'),
                ('tiktok', 'fab fa-tiktok text-dark')
            ]
            
            social_count = 0
            for platform, icon_class in social_platforms:
                url = getattr(team, platform)
                if url:
                    social_count += 1
                    social_html += f'<a href="{url}" target="_blank" class="social-link me-1" data-bs-toggle="tooltip" title="{platform.title()}"><i class="{icon_class}"></i></a>'
            
            if social_count == 0:
                social_html = '<span class="text-muted small">No links</span>'
            
            # Format dates
            created_html = team.created_at.strftime('%Y-%m-%d %H:%M')
            updated_html = team.updated_at.strftime('%Y-%m-%d %H:%M')
            
            # Display order
            order_html = f'<span class="badge bg-primary"><i class="fas fa-sort-numeric-down me-1"></i>{team.display_order}</span>'
            
            # Actions - check permissions for each action
            edit_url = reverse('teams_app:team_edit', args=[team.pk])
            delete_url = reverse('teams_app:team_delete', args=[team.pk])
            
            # Use the helper function to check permissions
            can_edit = can_modify_team(request.user, team)
            can_delete = can_modify_team(request.user, team) and (request.user.is_superuser or request.user.is_staff or request.user.has_perm('teams_app.delete_teams'))
            
            actions_html = '<div class="btn-group btn-group-sm" role="group">'
            
            if can_edit:
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit Team Member">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            
            if can_delete:
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{team.name}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Team Member">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            # Show message if no actions available
            if not can_edit and not can_delete:
                actions_html += '''
                    <span class="btn btn-outline-secondary disabled" data-bs-toggle="tooltip" title="No permissions">
                        <i class="fas fa-ban"></i>
                    </span>
                '''
            
            actions_html += '</div>'
            
            data.append({
                'image': image_html,
                'name': f'<strong>{team.name}</strong>',
                'designation': team.designation or '<span class="text-muted">Not set</span>',
                'email': f'<a href="mailto:{team.email}">{team.email}</a>',
                'phone': team.phone,
                'skills': f'<div class="team-skills">{skills_html}</div>',
                'social_links': f'<div class="team-social-links">{social_html}</div>',
                'description': description_html,
                'status': status_button,
                'display_order': order_html,
                'author': team.author.username,
                'created_at': f'<small>{created_html}</small>',
                'updated_at': f'<small>{updated_html}</small>',
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
        logger.error(f"Error in teams_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'Server error occurred'
        }, status=500)

@rbac_permission_required('teams_app.add_teams')
def team_create(request):
    """Create new team member - requires teams_app.add_teams permission"""
    if request.method == 'POST':
        form = TeamsForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.author = request.user
            team.save()
            messages.success(request, 'Team member created successfully!')
            return redirect('teams_app:teams_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamsForm()
    
    context = {
        'form': form,
        'page_title': 'Add Team Member',
        'breadcrumb_active': 'Add Team Member',
    }
    return render(request, 'teams/teams_form.html', context)

@login_required
def team_edit(request, pk):
    """Edit existing team member"""
    team = get_object_or_404(Teams, pk=pk)
    
    # Check if user can edit this specific team using helper function
    if not can_modify_team(request.user, team):
        messages.error(request, "You don't have permission to edit this team member.")
        return redirect('teams_app:teams_list')
    
    if request.method == 'POST':
        form = TeamsForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('teams_app:teams_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamsForm(instance=team)
    
    context = {
        'form': form,
        'team': team,
        'page_title': f'Edit Team Member - {team.name}',
        'breadcrumb_active': 'Edit Team Member',
    }
    return render(request, 'teams/teams_form.html', context)

@login_required
def team_delete(request, pk):
    """Delete team member"""
    team = get_object_or_404(Teams, pk=pk)
    
    # Check if user can delete this specific team using helper function
    if not can_modify_team(request.user, team):
        messages.error(request, "You don't have permission to delete this team member.")
        return redirect('teams_app:teams_list')
    
    if request.method == 'POST':
        team_name = team.name
        team.delete()
        messages.success(request, f'Team member "{team_name}" deleted successfully!')
        return redirect('teams_app:teams_list')
    
    context = {
        'team': team,
        'page_title': 'Delete Team Member',
        'breadcrumb_active': 'Delete Team Member'
    }
    return render(request, 'teams/teams_confirm_delete.html', context)

@login_required
def toggle_team_status(request, pk):
    """Toggle team status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            team = get_object_or_404(Teams, pk=pk)
            
            # Check if user can edit this specific team using helper function
            if not can_modify_team(request.user, team):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this team member status.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in ['active', 'inactive']:
                team.status = new_status
                team.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': team.status,
                    'new_status_display': team.get_status_display(),
                    'message': f'Team member status updated to {team.get_status_display()} successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid status provided'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Server error occurred'
            }, status=500)
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request'
    }, status=400)
