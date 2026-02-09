from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import strip_tags
from django.urls import reverse
from .models import Blog, BlogComment, Category
from .forms import BlogForm, BlogCommentForm, CategoryForm
from django.utils import timezone

def rbac_permission_required(permission):
    """
    Custom decorator for RBAC permission checking
    """
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            
            # Allow superusers and staff users
            if user.is_superuser or user.is_staff:
                return view_func(request, *args, **kwargs)

            # Check specific permission
            if user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            
            # Check role-based access
            if hasattr(user, 'role') and user.role and user.role.name == 'admin':
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "You don't have permission to access this page.")
            return redirect('bg_app:profile')
        return wrapped_view
    return decorator

def check_blog_permission(user, blog, permission):
    """
    Helper function to check if user has permission for a specific blog
    """
    if user.is_superuser or user.is_staff:
        return True
    if user.has_perm(permission):
        return True
    # Authors can edit/delete their own blogs
    if blog.author == user:
        return True
    return False

@rbac_permission_required('blog_app.view_blog')
def blog_list(request):
    """Blog list view - requires blog_app.view_blog permission"""
    context = {
        'page_title': 'Blog Posts List',
        'breadcrumb_active': 'Blog Posts List'
    }
    return render(request, 'blog/blog_list.html', context)

@rbac_permission_required('blog_app.view_blog')
def blogs_datatables(request):
    """Datatables AJAX endpoint - requires blog_app.view_blog permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Base queryset - superuser/staff can see all blogs, regular users only their own
        if request.user.is_superuser or request.user.is_staff:
            blogs = Blog.objects.all().select_related('category')
        else:
            blogs = Blog.objects.filter(author=request.user)
        
        # Total records count
        total_records = blogs.count()
        
        # Search functionality
        if search_value:
            blogs = blogs.filter(
                Q(title__icontains=search_value) |
                Q(short_description__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(slug__icontains=search_value) |
                Q(author__username__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = blogs.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'title',
            '1': 'image',
            '2': 'slug',
            '3': 'short_description',
            '4': 'status',
            '5': 'author__username',
            '6': 'created_at',
            '7': 'published_at',
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            blogs = blogs.order_by(order_field)
        else:
            blogs = blogs.order_by('-created_at')
        
        # Pagination
        blogs = blogs[start:start + length]
        
        # Prepare data for response
        data = []
        for blog in blogs:
            # Format short description with truncation
            short_desc = blog.short_description or ""
            short_desc_truncated = short_desc[:60] + "..." if len(short_desc) > 60 else short_desc
            
            # Format description with truncation
            plain_text = strip_tags(blog.description)
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
            
            # Render main image thumbnail
            image_html = '<span class="text-muted"><i class="fas fa-image"></i> No image</span>'
            if blog.image:
                try:
                    image_html = f'''
                        <img src="{blog.image.url}" alt="{blog.title}" 
                             class="img-thumbnail-table" 
                             data-bs-toggle="tooltip" 
                             title="{blog.title}">
                    '''
                except:
                    image_html = '<span class="text-danger"><i class="fas fa-exclamation-triangle"></i> Image error</span>'
            
            # Status badge
            status_badges = {
                'draft': '<span class="badge bg-secondary rounded-pill"><i class="fas fa-edit me-1"></i>Draft</span>',
                'published': '<span class="badge bg-success rounded-pill"><i class="fas fa-check-circle me-1"></i>Published</span>',
                'archived': '<span class="badge bg-warning rounded-pill"><i class="fas fa-archive me-1"></i>Archived</span>'
            }
            status_html = status_badges.get(blog.status, '<span class="badge bg-dark">Unknown</span>')
            
            # Status toggle button - only show if user has permission to edit this blog
            can_edit_blog = check_blog_permission(request.user, blog, 'blog_app.change_blog')
            status_button = ''
            if can_edit_blog:
                status_button = f'''
                    <div class="dropdown">
                        <button class="btn btn-sm status-toggle-btn {'btn-success' if blog.status == 'published' else 'btn-secondary' if blog.status == 'draft' else 'btn-warning'} dropdown-toggle"
                                type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas {'fa-check-circle' if blog.status == 'published' else 'fa-edit' if blog.status == 'draft' else 'fa-archive'} me-1"></i>
                            {blog.status.title()}
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="draft" data-blog-id="{blog.pk}"><i class="fas fa-edit me-2"></i>Draft</a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="published" data-blog-id="{blog.pk}"><i class="fas fa-check-circle me-2"></i>Published</a></li>
                            <li><a class="dropdown-item status-change-btn" href="#" data-status="archived" data-blog-id="{blog.pk}"><i class="fas fa-archive me-2"></i>Archived</a></li>
                        </ul>
                    </div>
                '''
            else:
                status_button = status_html
            
            # Format dates
            created_html = blog.created_at.strftime('%Y-%m-%d %H:%M')
            published_html = blog.published_at.strftime('%Y-%m-%d %H:%M') if blog.published_at else '<span class="text-muted">Not published</span>'
            
            # Reading time
            reading_time_html = f'<span class="badge bg-info"><i class="fas fa-clock me-1"></i>{blog.reading_time} min</span>'
            
            # Actions - only show actions user has permission for
            edit_url = reverse('blog_app:blog_edit', args=[blog.pk])
            delete_url = reverse('blog_app:blog_delete', args=[blog.pk])
            comments_url = reverse('blog_app:blog_comments', args=[blog.pk])
            view_url = reverse('blog_app:blog_detail', args=[blog.slug])
            
            # Check permissions for actions using helper function
            can_edit = check_blog_permission(request.user, blog, 'blog_app.change_blog')
            can_delete = check_blog_permission(request.user, blog, 'blog_app.delete_blog')
            can_manage_comments = request.user.is_superuser or request.user.is_staff or request.user.has_perm('blog_app.change_blogcomment')
            
            actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{view_url}" class="btn btn-outline-primary" target="_blank"
                       data-bs-toggle="tooltip" title="View Blog">
                        <i class="fas fa-eye"></i>
                    </a>
            '''
            
            if can_edit:
                actions_html += f'''
                    <a href="{edit_url}" class="btn btn-outline-warning" 
                       data-bs-toggle="tooltip" title="Edit Blog">
                        <i class="fas fa-edit"></i>
                    </a>
                '''
            
            if can_manage_comments:
                actions_html += f'''
                    <a href="{comments_url}" class="btn btn-outline-info" 
                       data-bs-toggle="tooltip" title="Manage Comments">
                        <i class="fas fa-comments"></i>
                    </a>
                '''
            
            if can_delete:
                actions_html += f'''
                    <a href="{delete_url}" class="btn btn-outline-danger" 
                       onclick="return confirm('Are you sure you want to delete \\'{blog.title}\\'?')"
                       data-bs-toggle="tooltip" title="Delete Blog">
                        <i class="fas fa-trash"></i>
                    </a>
                '''
            
            actions_html += '</div>'
            
            data.append({
                'title': f'<strong>{blog.title}</strong><br><small class="text-muted">{short_desc_truncated}</small>',
                'image': image_html,
                'slug': f'<code>{blog.slug}</code>',
                'description': description_html,
                'status': status_button,
                'status_badge': status_html,
                'author': blog.author.username,
                'reading_time': reading_time_html,
                'created_at': f'<i class="fas fa-calendar me-1"></i>{created_html}',
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
        logger.error(f"Error in blogs_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        }, status=500)

@rbac_permission_required('blog_app.add_blog')
def blog_create(request):
    """Create new blog post - requires blog_app.add_blog permission"""
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            
            # Handle publish/draft action
            action_type = request.POST.get('action_type')
            if action_type == 'publish':
                blog.status = Blog.Status.PUBLISHED
                if not blog.published_at:
                    blog.published_at = timezone.now()
                messages.success(request, 'Blog post published successfully!')
            else:  # draft
                blog.status = Blog.Status.DRAFT
                messages.success(request, 'Blog post saved as draft successfully!')
            
            blog.save()
            return redirect('blog_app:blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    
    context = {
        'form': form,
        'page_title': 'Create Blog Post',
        'breadcrumb_active': 'Create Blog Post'
    }
    return render(request, 'blog/blog_form.html', context)

@login_required
def blog_edit(request, pk):
    """Edit existing blog post - user can edit own blogs, admin/staff can edit all"""
    blog = get_object_or_404(Blog, pk=pk)
    
    # Check permission using helper function
    if not check_blog_permission(request.user, blog, 'blog_app.change_blog'):
        messages.error(request, 'You do not have permission to edit this blog post.')
        return redirect('blog_app:blog_list')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            
            # Handle publish/draft action
            action_type = request.POST.get('action_type')
            if action_type == 'publish':
                blog.status = Blog.Status.PUBLISHED
                if not blog.published_at:
                    blog.published_at = timezone.now()
                messages.success(request, 'Blog post published successfully!')
            else:  # draft
                blog.status = Blog.Status.DRAFT
                messages.success(request, 'Blog post saved as draft successfully!')
            
            blog.save()
            return redirect('blog_app:blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm(instance=blog)
    
    context = {
        'form': form,
        'blog': blog,
        'page_title': 'Edit Blog Post',
        'breadcrumb_active': 'Edit Blog Post'
    }
    return render(request, 'blog/blog_form.html', context)

@login_required
def blog_delete(request, pk):
    """Delete blog post - user can delete own blogs, admin/staff can delete all"""
    blog = get_object_or_404(Blog, pk=pk)
    
    # Check permission using helper function
    if not check_blog_permission(request.user, blog, 'blog_app.delete_blog'):
        messages.error(request, 'You do not have permission to delete this blog post.')
        return redirect('blog_app:blog_list')
    
    if request.method == 'POST':
        blog_title = blog.title
        blog.delete()
        messages.success(request, f'Blog post "{blog_title}" deleted successfully!')
        return redirect('blog_app:blog_list')
    
    context = {
        'blog': blog,
        'page_title': 'Delete Blog Post',
        'breadcrumb_active': 'Delete Blog Post'
    }
    return render(request, 'blog/blog_confirm_delete.html', context)

@login_required
def toggle_blog_status(request, pk):
    """Toggle blog status via AJAX"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            blog = get_object_or_404(Blog, pk=pk)
            
            # Check permission using helper function
            if not check_blog_permission(request.user, blog, 'blog_app.change_blog'):
                return JsonResponse({
                    'success': False,
                    'error': 'You do not have permission to change the status of this blog post.'
                })
            
            new_status = request.POST.get('status')
            
            if new_status in dict(Blog.Status.choices):
                blog.status = new_status
                if new_status == 'published' and not blog.published_at:
                    blog.published_at = timezone.now()
                blog.save()
                
                return JsonResponse({
                    'success': True,
                    'new_status': blog.status,
                    'message': f'Blog status updated to {blog.get_status_display()} successfully!'
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

# Blog Comments Management View
@rbac_permission_required('blog_app.view_blogcomment')
def blog_comments(request, pk):
    """Manage blog comments - requires blog_app.view_blogcomment permission"""
    blog = get_object_or_404(Blog, pk=pk)
    
    # Get all comments for this blog
    comments = blog.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')
        
        if comment_id and action:
            try:
                comment = BlogComment.objects.get(pk=comment_id, blog=blog)
                
                # Check permission for comment management
                if not (request.user.is_superuser or request.user.is_staff):
                    messages.error(request, 'You do not have permission to manage comments.')
                    return redirect('blog_app:blog_comments', pk=blog.pk)
                
                if action == 'approve':
                    comment.status = BlogComment.Status.APPROVED
                    comment.save()
                    messages.success(request, 'Comment approved successfully!')
                elif action == 'reject':
                    comment.status = BlogComment.Status.REJECTED
                    comment.save()
                    messages.success(request, 'Comment rejected successfully!')
                elif action == 'delete':
                    comment_text = comment.comment
                    comment.delete()
                    messages.success(request, f'Comment "{comment_text[:50]}..." deleted successfully!')
                    
            except BlogComment.DoesNotExist:
                messages.error(request, 'Comment not found!')
        
        return redirect('blog_app:blog_comments', pk=blog.pk)
    
    # Count comments by status for display
    comment_stats = {
        'total': comments.count(),
        'approved': comments.filter(status='approved').count(),
        'pending': comments.filter(status='pending').count(),
        'rejected': comments.filter(status='rejected').count(),
    }
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_stats': comment_stats,
        'page_title': f'Manage Comments - {blog.title}',
        'breadcrumb_active': 'Manage Comments'
    }
    return render(request, 'blog/blog_comments.html', context)

@login_required
def blog_comments_delete(request, pk=None, comment_id=None):
    """
    Delete a specific comment from a blog post.
    """
    # If accessed without parameters, redirect to blog list
    if request.method == 'GET' and (pk is None or comment_id is None):
        messages.error(request, 'Invalid access to comment deletion.')
        return redirect('blog_app:blog_list')
    
    blog = get_object_or_404(Blog, pk=pk)
    comment = get_object_or_404(BlogComment, pk=comment_id, blog=blog)
    
    # Authorization: Comment author, superusers, or staff can delete comments
    if not (comment.user == request.user or 
            request.user.is_superuser or 
            request.user.is_staff):
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('blog_app:blog_detail', slug=blog.slug)

    if request.method == 'POST':
        comment_text = comment.comment
        comment.delete()
        messages.success(request, f'Comment "{comment_text[:50]}..." deleted successfully!')
        return redirect('blog_app:blog_detail', slug=blog.slug)

    context = {
        'blog': blog,
        'comment': comment,
        'page_title': 'Delete Comment',
        'breadcrumb_active': 'Delete Comment'
    }
    return render(request, 'blog/comment_confirm_delete.html', context)

def blog_detail(request, slug):
    """Public blog detail view - no authentication required"""
    # Add a check to prevent 'categories' from being treated as a blog slug
    if slug == 'categories':
        return redirect('blog_app:category_list')
    
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    # Get approved comments only for public view
    comments = blog.comments.filter(status=BlogComment.Status.APPROVED).order_by('-created_at')
    
    # Handle comment submission (both logged-in and non-logged-in users)
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validation
        if len(comment_text) < 10:
            messages.error(request, 'Comment must be at least 10 characters long.')
        elif len(comment_text) > 1000:
            messages.error(request, 'Comment cannot exceed 1000 characters.')
        elif not full_name:
            messages.error(request, 'Please provide your full name.')
        elif not email:
            messages.error(request, 'Please provide your email address.')
        else:
            # Create comment - default status is PENDING (not displayed until approved)
            BlogComment.objects.create(
                blog=blog,
                comment=comment_text,
                full_name=full_name,
                email=email,
                status=BlogComment.Status.PENDING  # Comments require approval
            )
            messages.success(request, 'Your comment has been submitted and is awaiting approval!')
            return redirect('blog_app:blog_detail', slug=blog.slug)
    
    context = {
        'blog': blog,
        'comments': comments,
        'page_title': blog.title,
    }
    return render(request, 'blog/blog_detail.html', context)

# AJAX view for quick comment moderation
@login_required
def ajax_comment_action(request):
    """Handle AJAX requests for comment actions"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            comment_id = request.POST.get('comment_id')
            action = request.POST.get('action')
            
            if not comment_id or not action:
                return JsonResponse({'success': False, 'error': 'Missing parameters'})
            
            comment = get_object_or_404(BlogComment, id=comment_id)
            
            # Check permission - only superusers, staff, or users with specific permissions
            if not (request.user.is_superuser or request.user.is_staff or 
                    request.user.has_perm('blog_app.change_blogcomment')):
                return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            if action == 'approve':
                comment.status = BlogComment.Status.APPROVED
                comment.save()
                return JsonResponse({
                    'success': True, 
                    'message': 'Comment approved',
                    'new_status': 'approved'
                })
            
            elif action == 'reject':
                comment.status = BlogComment.Status.REJECTED
                comment.save()
                return JsonResponse({
                    'success': True, 
                    'message': 'Comment rejected',
                    'new_status': 'rejected'
                })
            
            elif action == 'delete':
                comment_text = comment.comment
                comment.delete()
                return JsonResponse({'success': True, 'message': 'Comment deleted'})
            
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# Category List View
@rbac_permission_required('blog_app.view_category')
def category_list(request):
    """Category list view - requires blog_app.view_category permission"""
    context = {
        'page_title': 'Categories List',
        'breadcrumb_active': 'Categories List'
    }
    return render(request, 'blog/category_list.html', context)

@rbac_permission_required('blog_app.view_category')
def categories_datatables(request):
    """Datatables AJAX endpoint for categories - requires blog_app.view_category permission"""
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Base queryset
        categories = Category.objects.all()
        
        # Total records count
        total_records = categories.count()
        
        # Search functionality
        if search_value:
            categories = categories.filter(
                Q(name__icontains=search_value) |
                Q(slug__icontains=search_value) |
                Q(description__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = categories.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'name',
            '1': 'slug',
            '2': 'description',
            '3': 'created_at',
        }
        
        order_field = column_map.get(order_column_index, 'name')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            categories = categories.order_by(order_field)
        else:
            categories = categories.order_by('name')
        
        # Pagination
        categories = categories[start:start + length]
        
        # Prepare data for response
        data = []
        for category in categories:
            # Format description with truncation
            description = category.description or ""
            description_truncated = description[:80] + "..." if len(description) > 80 else description
            
            # Count blogs in this category
            blog_count = Blog.objects.filter(category=category).count()
            
            # Format dates
            created_html = category.created_at.strftime('%Y-%m-%d %H:%M')
            
            # Actions - only show actions user has permission for
            edit_url = reverse('blog_app:category_edit', args=[category.pk])
            delete_url = reverse('blog_app:category_delete', args=[category.pk])
            
            # Check permissions for actions
            can_edit = request.user.has_perm('blog_app.change_category')
            can_delete = request.user.has_perm('blog_app.delete_category')
            
            # Fix: Proper onclick handling
            delete_onclick = ""
            if can_delete:
                delete_onclick = f"return confirm('Are you sure you want to delete \\\"{category.name}\\\"?')"
            else:
                delete_onclick = "return false;"
            
            actions_html = f'''
                <div class="btn-group btn-group-sm" role="group">
                    <a href="{edit_url}" class="btn btn-outline-warning {'disabled' if not can_edit else ''}" 
                       data-bs-toggle="tooltip" title="Edit Category" {'onclick="return false;"' if not can_edit else ''}>
                        <i class="fas fa-edit"></i>
                    </a>
                    <a href="{delete_url}" class="btn btn-outline-danger {'disabled' if not can_delete else ''}" 
                       onclick="{delete_onclick}"
                       data-bs-toggle="tooltip" title="Delete Category">
                        <i class="fas fa-trash"></i>
                    </a>
                </div>
            '''
            
            data.append({
                'name': f'<strong>{category.name}</strong>',
                'slug': f'<code>{category.slug}</code>',
                'description': f'<span class="text-muted">{description_truncated}</span>',
                'blog_count': f'<span class="badge bg-primary">{blog_count} blog(s)</span>',
                'created_at': f'<i class="fas fa-calendar me-1"></i>{created_html}',
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
        logger.error(f"Error in categories_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'error': str(e)
        }, status=500)

@rbac_permission_required('blog_app.add_category')
def category_create(request):
    """Create new category - requires blog_app.add_category permission"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('blog_app:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'page_title': 'Create Category',
        'breadcrumb_active': 'Create Category'
    }
    return render(request, 'blog/category_form.html', context)

@rbac_permission_required('blog_app.change_category')
def category_edit(request, pk):
    """Edit existing category - requires blog_app.change_category permission"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('blog_app:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'page_title': 'Edit Category',
        'breadcrumb_active': 'Edit Category'
    }
    return render(request, 'blog/category_form.html', context)

@rbac_permission_required('blog_app.delete_category')
def category_delete(request, pk):
    """Delete category - requires blog_app.delete_category permission"""
    category = get_object_or_404(Category, pk=pk)
    
    # Check if category has associated blogs
    blog_count = Blog.objects.filter(category=category).count()
    
    if request.method == 'POST':
        if blog_count > 0:
            # If there are associated blogs, don't allow deletion
            messages.error(request, f'Cannot delete category "{category.name}" because it has {blog_count} associated blog(s). Please reassign or delete those blogs first.')
            return redirect('blog_app:category_list')
        
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('blog_app:category_list')
    
    context = {
        'category': category,
        'blog_count': blog_count,
        'page_title': 'Delete Category',
        'breadcrumb_active': 'Delete Category'
    }
    return render(request, 'blog/category_confirm_delete.html', context)