import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import strip_tags
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Course, Media,CourseEnrollment
from .forms import CourseForm, MediaForm, MediaInlineFormSet
from bg_app.decorators import rbac_permission_required

# Helper function to check if user can modify specific course - FIXED
def can_modify_course(user, course):
    """
    Check if user can modify specific course 
    - Superusers: always can modify
    - Staff: only if they have explicit permissions
    - Regular users: can only modify their own courses
    """
    if user.is_superuser:
        return True
    
    # Staff users require explicit permissions
    if user.is_staff:
        # Check if staff has global change permission
        if user.has_perm('course_app.change_course'):
            return True
        return False
    
    # Regular users can only modify their own courses
    return course.author == user

# Helper function to check if user can delete specific course - FIXED
def can_delete_course(user, course):
    """
    Check if user can delete specific course
    """
    if user.is_superuser:
        return True
    
    # Staff users require explicit delete permission
    if user.is_staff:
        return user.has_perm('course_app.delete_course')
    
    # Regular users can only delete their own courses if they have delete permission
    if course.author == user:
        return user.has_perm('course_app.delete_course')
    
    return False

# Helper function to get base queryset based on user permissions - FIXED
def get_courses_queryset(user):
    """
    Return appropriate queryset based on user permissions:
    - Superusers: all courses
    - Staff with view_course permission: all courses  
    - Regular users: only their own courses
    """
    if user.is_superuser:
        return Course.objects.all()
    
    if user.is_staff:
        if user.has_perm('course_app.view_course'):
            return Course.objects.all()
        # Staff without view permission see nothing
        return Course.objects.none()
    
    # Regular users without global view permission can only see their own
    if user.has_perm('course_app.view_course'):
        return Course.objects.all()
    
    return Course.objects.filter(author=user)

@rbac_permission_required('course_app.view_course')
def courses_list(request):
    """Courses list view - requires course_app.view_course permission"""
    context = {
        'page_title': 'Course Management',
        'breadcrumb_active': 'Course List',
        'can_create_course': request.user.has_perm('course_app.add_course'),
    }
    return render(request, 'courses/courses_list.html', context)

@rbac_permission_required('course_app.view_course')
def courses_datatables(request):
    """Datatables AJAX endpoint - requires course_app.view_course permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Get appropriate queryset based on user permissions
        courses = get_courses_queryset(request.user)
        
        # Total records count
        total_records = courses.count()
        
        # Search functionality
        if search_value:
            courses = courses.filter(
                Q(title__icontains=search_value) |
                Q(short_description__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(author__username__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = courses.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'title',
            '1': 'duration', 
            '2': 'price',
            '3': 'status',
            '4': 'author__username',
            '5': 'created_at',
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            courses = courses.order_by(order_field)
        else:
            courses = courses.order_by('-created_at')
        
        # Pagination
        courses = courses[start:start + length]
        
        # Prepare data for response
        data = []
        for course in courses:
            # Format description with truncation
            plain_text = strip_tags(course.description)
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
            
            # Short description display
            short_desc = course.short_description[:80] + "..." if len(course.short_description) > 80 else course.short_description
            
            # Image display
            if course.image:
                image_html = f'<img src="{course.image.url}" alt="{course.title}" class="rounded" width="60" height="45" style="object-fit: cover;">'
            else:
                image_html = '''
                    <div class="rounded d-flex align-items-center justify-content-center bg-light border" 
                         style="width: 60px; height: 45px;">
                        <i class="fas fa-book text-muted"></i>
                    </div>
                '''
            
            # Price display
            if course.has_discount():
                price_html = f'''
                    <div>
                        <span class="text-muted text-decoration-line-through me-2">₹ {course.price}</span>
                        <strong class="text-success">₹ {course.offer_price}</strong>
                        <span class="badge bg-danger ms-1">-{course.discount_percentage()}%</span>
                    </div>
                '''
            else:
                price_html = f'<strong>₹ {course.price}</strong>'
            
            # Duration display
            duration_html = f'<span class="badge bg-info"><i class="fas fa-clock me-1"></i>{course.duration_display()}</span>'
            
            # Media count
            media_count = course.media.filter(status=True).count()
            media_html = f'''
                <span class="badge bg-secondary" data-bs-toggle="tooltip" title="{media_count} media files">
                    <i class="fas fa-photo-video me-1"></i>{media_count}
                </span>
            '''
            
            # Status display
            if course.status:
                status_html = '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Active</span>'
            else:
                status_html = '<span class="badge bg-danger rounded-pill"><i class="fas fa-times-circle me-1"></i>Inactive</span>'
            
            # Status toggle button - only if user has change permission for this course
            can_change_course = can_modify_course(request.user, course)
            
            status_button = ''
            if can_change_course:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm {'btn-success' if course.status else 'btn-danger'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas {'fa-check-circle' if course.status else 'fa-times-circle'} me-1"></i>
                            {'Active' if course.status else 'Inactive'}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="true" data-course-id="{course.pk}">
                                <i class="fas fa-check-circle me-2 text-success"></i>Active
                            </a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="false" data-course-id="{course.pk}">
                                <i class="fas fa-times-circle me-2 text-danger"></i>Inactive
                            </a></li>
                        </ul>
                    </div>
                '''
            else:
                status_button = status_html
            
            # Format dates
            created_html = course.created_at.strftime('%Y-%m-%d %H:%M')
            updated_html = course.updated_at.strftime('%Y-%m-%d %H:%M')
            
            # Action URLs - FIXED: Changed 'course_media' to 'course_media_list'
            view_url = reverse('course_app:course_detail', args=[course.pk])
            edit_url = reverse('course_app:course_edit', args=[course.pk])
            delete_url = reverse('course_app:course_delete', args=[course.pk])
            media_url = reverse('course_app:course_media_list', args=[course.pk])  # FIXED THIS LINE
            
            actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{media_url}" class="btn btn-outline-info" 
                       data-bs-toggle="tooltip" title="Manage Media">
                        <i class="fas fa-photo-video"></i>
                    </a>
                    
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit Course">
                        <i class="fas fa-edit"></i>
                    </a>
                    
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{course.title}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Course">
                        <i class="fas fa-trash"></i>
                    </a>

                    <a href="{view_url}" class="btn btn-outline-secondary" 
                       data-bs-toggle="tooltip" title="View Details">
                        <i class="fas fa-eye"></i>
                    </a>
                    
                </div>
            '''
            
            data.append({
                'image': image_html,
                'title': f'<strong>{course.title}</strong><br><small class="text-muted">{short_desc}</small>',
                'duration': duration_html,
                'price': price_html,
                'media_count': media_html,
                'description': description_html,
                'status': status_button,
                'author': course.author.username,
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
        logger.error(f"Error in courses_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': 'Server error occurred'
        }, status=500)

@rbac_permission_required('course_app.add_course')
def course_create(request):
    """Create new course - requires course_app.add_course permission"""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                course = form.save(commit=False)
                course.author = request.user  
                course.save()
                messages.success(request, 'Course created successfully!')
                return redirect('course_app:courses_list')
            except Exception as e:
                messages.error(request, f'Error creating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'page_title': 'Add Course',
        'breadcrumb_active': 'Add Course',
    }
    return render(request, 'courses/courses_form.html', context)

@rbac_permission_required('course_app.change_course')
def course_edit(request, pk):
    """Edit existing course - requires course_app.change_course permission"""
    course = get_object_or_404(Course, pk=pk)
    
    # Additional check: user must be able to modify this specific course
    if not can_modify_course(request.user, course):
        messages.error(request, "You don't have permission to edit this course.")
        return redirect('course_app:courses_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_app:courses_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'page_title': f'Edit Course - {course.title}',
        'breadcrumb_active': 'Edit Course',
    }
    return render(request, 'courses/courses_form.html', context)

@rbac_permission_required('course_app.delete_course')
def course_delete(request, pk):
    """Delete course - requires course_app.delete_course permission"""
    course = get_object_or_404(Course, pk=pk)
    
    # Additional check: user must be able to delete this specific course
    if not can_delete_course(request.user, course):
        messages.error(request, "You don't have permission to delete this course.")
        return redirect('course_app:courses_list')
    
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Course "{course_title}" deleted successfully!')
        return redirect('course_app:courses_list')
    
    context = {
        'course': course,
        'page_title': 'Delete Course',
        'breadcrumb_active': 'Delete Course'
    }
    return render(request, 'courses/courses_confirm_delete.html', context)

# Helper function to check if user can manage media for specific course
def can_manage_course_media(user, course):
    """
    Check if user can manage media for specific course 
    - Superusers: always can manage
    - Staff with change_media permission: can manage media for all courses
    - Regular users: can only manage media for their own courses
    """
    if user.is_superuser:
        return True
    
    # Staff users require explicit media permissions
    if user.is_staff:
        return user.has_perm('course_app.change_media')
    
    # Regular users can only manage media for their own courses
    return course.author == user

@rbac_permission_required('course_app.view_media')
def course_media_list(request, pk):
    """List all media for a course"""
    course = get_object_or_404(Course, pk=pk)
    
    media_list = course.media.all().order_by('order', 'created_at')
    active_media_count = media_list.filter(status=True).count()
    
    context = {
        'course': course,
        'media_list': media_list,
        'page_title': f'Manage Media - {course.title}',
        'breadcrumb_active': 'Manage Media',
        'active_media_count': active_media_count,
        'media_permissions': {
            'can_add': request.user.has_perm('course_app.add_media'),
            'can_change': request.user.has_perm('course_app.change_media'),
            'can_delete': request.user.has_perm('course_app.delete_media'),
            'can_view': request.user.has_perm('course_app.view_media'),
        }
    }
    return render(request, 'courses/courses_media.html', context)

@rbac_permission_required('course_app.add_media')
def media_create(request, course_pk):
    """Create new media for a course"""
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.method == 'POST':
        # Check if form has course field
        form_has_course_field = 'course' in MediaForm().fields
        
        if form_has_course_field:
            # Form expects course field, so include it
            post_data = request.POST.copy()
            post_data['course'] = course.pk
            form = MediaForm(post_data, request.FILES)
        else:
            # Form doesn't have course field
            form = MediaForm(request.POST, request.FILES)
        
        if form.is_valid():
            media = form.save(commit=False)
            media.course = course  # Always set the course
            
            # Set order if not provided
            if not media.order:
                last_media = course.media.order_by('-order').first()
                media.order = (last_media.order + 1) if last_media else 1
            
            try:
                media.save()
                messages.success(request, 'Media added successfully!')
                return redirect('course_app:course_media_list', pk=course_pk)
            except Exception as e:
                messages.error(request, f'Error saving media: {str(e)}')
        else:
            # Log errors for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Media form errors: {form.errors}")
            
            # Show specific error messages
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if field in form.fields else field
                    error_messages.append(f"{field_name}: {error}")
            
            if error_messages:
                messages.error(request, f"Please correct the following errors: {', '.join(error_messages)}")
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # Initialize form for GET request
        form_has_course_field = 'course' in MediaForm().fields
        if form_has_course_field:
            form = MediaForm(initial={'course': course})
        else:
            form = MediaForm()
    
    context = {
        'course': course,
        'form': form,
        'page_title': f'Add Media - {course.title}',
        'breadcrumb_active': 'Add Media',
        'form_has_course_field': 'course' in form.fields,  # Pass to template
    }
    return render(request, 'courses/media_form.html', context)

@rbac_permission_required('course_app.change_media')
def media_update(request, course_pk, media_pk):
    """Update existing media"""
    course = get_object_or_404(Course, pk=course_pk)
    media = get_object_or_404(Media, pk=media_pk, course=course)
    
    if request.method == 'POST':
        # Check if form has course field
        form_has_course_field = 'course' in MediaForm().fields
        
        if form_has_course_field:
            # Form expects course field, so include it
            post_data = request.POST.copy()
            post_data['course'] = course.pk
            form = MediaForm(post_data, request.FILES, instance=media)
        else:
            # Form doesn't have course field
            form = MediaForm(request.POST, request.FILES, instance=media)
        
        if form.is_valid():
            updated_media = form.save(commit=False)
            updated_media.course = course  # Always set the course
            
            # Handle file: if no new file, keep existing
            if 'file' not in request.FILES or not request.FILES.get('file'):
                updated_media.file = media.file
            
            try:
                updated_media.save()
                messages.success(request, 'Media updated successfully!')
                return redirect('course_app:course_media_list', pk=course_pk)
            except Exception as e:
                messages.error(request, f'Error updating media: {str(e)}')
        else:
            # Log errors for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Media form errors: {form.errors}")
            
            # Show specific error messages
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = form.fields[field].label if field in form.fields else field
                    error_messages.append(f"{field_name}: {error}")
            
            if error_messages:
                messages.error(request, f"Please correct the following errors: {', '.join(error_messages)}")
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        # Initialize form for GET request
        form_has_course_field = 'course' in MediaForm().fields
        if form_has_course_field:
            form = MediaForm(instance=media, initial={'course': course})
        else:
            form = MediaForm(instance=media)
    
    context = {
        'course': course,
        'media': media,
        'form': form,
        'page_title': f'Edit Media - {course.title}',
        'breadcrumb_active': 'Edit Media',
        'form_has_course_field': 'course' in form.fields,  # Pass to template
    }
    return render(request, 'courses/media_form.html', context)

@rbac_permission_required('course_app.delete_media')
def media_delete(request, course_pk, media_pk):
    """Delete media"""
    course = get_object_or_404(Course, pk=course_pk)
    media = get_object_or_404(Media, pk=media_pk, course=course)
    
    if request.method == 'POST':
        media_title = media.caption or media.file.name
        media.delete()
        messages.success(request, f'Media "{media_title}" deleted successfully!')
        return redirect('course_app:course_media_list', pk=course_pk)
    
    context = {
        'course': course,
        'media': media,
        'page_title': 'Delete Media',
        'breadcrumb_active': 'Delete Media'
    }
    return render(request, 'courses/media_confirm_delete.html', context)

@login_required
def toggle_media_status(request, course_pk, media_pk):
    """Toggle media status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            course = get_object_or_404(Course, pk=course_pk)
            media = get_object_or_404(Media, pk=media_pk, course=course)
            
            # Check global permission first
            if not request.user.has_perm('course_app.change_media'):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change media status.'
                }, status=403)
            
            # Check if user can edit this specific media
            if not can_manage_course_media(request.user, course):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this media status.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in ['true', 'false']:
                media.status = (new_status == 'true')
                media.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': media.status,
                    'new_status_display': 'Active' if media.status else 'Inactive',
                    'message': f'Media status updated to {"Active" if media.status else "Inactive"} successfully!'
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

@login_required
def toggle_course_status(request, pk):
    """Toggle course status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            course = get_object_or_404(Course, pk=pk)
            
            # Check if user can edit this specific course using helper function
            if not can_modify_course(request.user, course):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change this course status.'
                }, status=403)
            
            new_status = request.POST.get('status')
            
            if new_status in ['true', 'false']:
                course.status = (new_status == 'true')
                course.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': course.status,
                    'new_status_display': 'Active' if course.status else 'Inactive',
                    'message': f'Course status updated to {"Active" if course.status else "Inactive"} successfully!'
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

@login_required
def course_detail(request, pk):
    """Course detail view"""
    try:
        course = get_object_or_404(Course, pk=pk)
        
        # Check if user has permission to view this course
        if not can_modify_course(request.user, course) and not request.user.has_perm('course_app.view_course'):
            messages.error(request, "You don't have permission to view this course.")
            return redirect('course_app:courses_list')
        
        # Get recent enrollments
        recent_enrollments = course.enrollments.all().order_by('-enrolled_at')[:5]
        
        # Get active media count
        active_media_count = course.media.filter(status=True).count()
        
        # Check if user can view enrollments
        can_view_enrollments = (
            request.user.has_perm('course_app.view_courseenrollment') and 
            can_modify_course(request.user, course)
        )
        
        context = {
            'course': course,
            'recent_enrollments': recent_enrollments,
            'active_media_count': active_media_count,
            'can_view_enrollments': can_view_enrollments,
            'page_title': f'Course Details - {course.title}',
            'breadcrumb_active': 'Course Details',
        }
        
        return render(request, 'courses/course_detail.html', context)
        
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    except Exception as e:
        messages.error(request, f"Error loading course details: {str(e)}")
        return redirect('course_app:courses_list')

@login_required
def course_enroll_datatable(request, pk):
    """Datatables AJAX endpoint for course enrollments"""
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get the course object
            course = get_object_or_404(Course, pk=pk)  
            
            # Get DataTables parameters
            draw = int(request.GET.get('draw', 1))
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search[value]', '').strip()
            order_column_index = request.GET.get('order[0][column]', '0')
            order_direction = request.GET.get('order[0][dir]', 'asc')
            
            # Get enrollments for this course
            enrollments = CourseEnrollment.objects.filter(course=course)
            
            # Total records count
            total_records = enrollments.count()
            
            # Search functionality
            if search_value:
                enrollments = enrollments.filter(
                    Q(first_name__icontains=search_value) |
                    Q(last_name__icontains=search_value) |
                    Q(email__icontains=search_value) |
                    Q(contact_number__icontains=search_value) |
                    Q(address__icontains=search_value)
                )
            
            # Filtered records count
            filtered_records = enrollments.count()
            
            # Column mapping for ordering
            column_map = {
                '0': 'first_name',
                '1': 'email',
                '2': 'contact_number',
                '3': 'education',
                '4': 'experience',
                '5': 'enrolled_at',
            }
            
            order_field = column_map.get(order_column_index, 'enrolled_at')
            if order_field:
                if order_direction == 'desc':
                    order_field = '-' + order_field
                enrollments = enrollments.order_by(order_field)
            else:
                enrollments = enrollments.order_by('-enrolled_at')
            
            # Pagination
            enrollments = enrollments[start:start + length]
            
            # Prepare data for response
            data = []
            for enrollment in enrollments:
                # Format education and experience for display
                education_display = enrollment.get_education_display() if enrollment.education else 'Not specified'
                experience_display = enrollment.get_experience_display() if enrollment.experience else 'Not specified'
                source_display = enrollment.get_source_display() if enrollment.source else 'Not specified'
                
                # Truncate address for display (using Python string slicing instead of truncatewords)
                address_display = enrollment.address
                if address_display and len(address_display) > 50:
                    address_display = address_display[:50] + '...'
                
                # Status badge
                if enrollment.status:
                    status_html = '<span class="badge bg-success">Active</span>'
                else:
                    status_html = '<span class="badge bg-danger">Inactive</span>'
                
                # Action URLs - attempt to reverse with both ids, fallback safely if pattern differs
                try:
                    from django.urls import NoReverseMatch
                    try:
                        delete_url = reverse('course_app:course_enroll_delete', args=[course.pk, enrollment.pk])
                    except NoReverseMatch:
                        # fallback to attempt reverse with only course pk (if URL pattern expects only one arg)
                        try:
                            delete_url = reverse('course_app:course_enroll_delete', args=[course.pk])
                        except Exception:
                            # final fallback to a harmless anchor so datatable renders without raising
                            delete_url = '#'
                except Exception:
                    delete_url = '#'

                # Action buttons
                actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{enrollment.first_name}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Course">
                        <i class="fas fa-trash"></i>
                    </a>

                 </div>
                '''
                
                data.append({
                    'id': enrollment.id,
                    'student': f'''
                        <strong>{enrollment.full_name}</strong>
                        <br>
                        <small class="text-muted">{enrollment.email}</small>
                    ''',
                    'contact': f'''
                        <strong>{enrollment.contact_number}</strong>
                        <br>
                        <small class="text-muted">{address_display}</small>
                    ''',
                    'education': f'<span class="badge bg-light text-dark">{education_display}</span>',
                    'experience': f'<span class="badge bg-info">{experience_display}</span>',
                    'source': f'<span class="badge bg-secondary">{source_display}</span>',
                    'enrolled_at': enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M'),
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
            logger.error(f"Error in course_enroll_datatable: {str(e)}")
            
            return JsonResponse({
                'draw': 1,
                'recordsTotal': 0,
                'recordsFiltered': 0,
                'data': [],
                'error': 'Server error occurred'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@rbac_permission_required('course_app.delete_courseenrollment')
def course_enroll_delete(request, pk, enrollment_pk):
    """Delete a course enrollment (with confirmation / AJAX support)"""
    try:
        course = get_object_or_404(Course, pk=pk)
        enrollment = get_object_or_404(CourseEnrollment, pk=enrollment_pk, course=course)

        # Ensure the user can modify/delete this course's data
        if not can_modify_course(request.user, course):
            messages.error(request, "You don't have permission to delete this enrollment.")
            return redirect('course_app:course_detail', pk=pk)

        # AJAX delete
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                title = enrollment.full_name if getattr(enrollment, 'full_name', None) else enrollment.email or str(enrollment.id)
                enrollment.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'Enrollment for \"{title}\" deleted successfully!',
                })
            except Exception:
                return JsonResponse({'success': False, 'error': 'Server error occurred'}, status=500)

        # Standard POST delete (form submission)
        if request.method == 'POST':
            title = enrollment.full_name if getattr(enrollment, 'full_name', None) else enrollment.email or str(enrollment.id)
            enrollment.delete()
            messages.success(request, f'Enrollment for "{title}" deleted successfully!')
            return redirect('course_app:course_detail', pk=pk)

        # Render confirmation page
        context = {
            'course': course,
            'enrollment': enrollment,
            'page_title': 'Delete Enrollment',
            'breadcrumb_active': 'Delete Enrollment'
        }
        return render(request, 'courses/enrollment_confirm_delete.html', context)

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error in course_enroll_delete: {str(e)}")
        messages.error(request, 'Error deleting enrollment.')
        return redirect('course_app:course_detail', pk=pk)