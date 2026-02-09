from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.utils.html import strip_tags
from .models import Training, TrainingImage
from .forms import TrainingForm, TrainingImageFormSet
# Import from bg_app for RBAC
from bg_app.decorators import rbac_permission_required, rbac_role_required
from bg_app.views import rbac_permission_required

import json

def format_price(price):
    """Helper function to format price with Indian Rupee symbol"""
    return f'₹{price:,}'

@rbac_permission_required('trainings_app.view_training')
def training_list(request):
    context = {
        'page_title': 'Trainings List',
        'breadcrumb_active': 'Trainings List'
    }
    return render(request, 'trainings/training_list.html', context)

@rbac_permission_required('trainings_app.view_training')
def trainings_datatables(request):
    try:
        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()
        order_column_index = request.GET.get('order[0][column]', '0')
        order_direction = request.GET.get('order[0][dir]', 'asc')
        
        # Base queryset - superusers/staff see all, others see only active
        if request.user.is_superuser or request.user.is_staff:
            trainings = Training.objects.all()
        else:
            trainings = Training.objects.filter(status=True)
        
        # Total records count
        total_records = trainings.count()
        
        # Search functionality
        if search_value:
            trainings = trainings.filter(
                Q(title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(duration__icontains=search_value)
            )
        
        # Filtered records count
        filtered_records = trainings.count()
        
        # Column mapping for ordering
        column_map = {
            '0': 'title',
            '1': 'image',
            '2': 'duration',
            '3': 'description',
            '4': 'price',
            '5': 'offer_price',
            '6': 'discount',
            '7': 'status',
            '8': 'created_at',
        }
        
        order_field = column_map.get(order_column_index, 'created_at')
        if order_field:
            if order_direction == 'desc':
                order_field = '-' + order_field
            trainings = trainings.order_by(order_field)
        else:
            trainings = trainings.order_by('-created_at')
        
        # Pagination
        trainings = trainings[start:start + length]
        
        # Prepare data for response
        data = []
        for training in trainings:
            # Format description with truncation
            plain_text = strip_tags(training.description)
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
            if training.image:
                try:
                    image_html = f'''
                        <img src="{training.image.url}" alt="{training.title}" 
                             class="img-thumbnail-table" 
                             data-bs-toggle="tooltip" 
                             title="{training.title}">
                    '''
                except:
                    image_html = '<span class="text-danger"><i class="fas fa-exclamation-triangle"></i> Image error</span>'
            
            # Format duration
            duration_display = str(training.duration)
            
            # Format prices
            price_html = f'<span class="price-text">{format_price(training.price)}</span>'
            
            if training.has_offer:
                offer_html = f'<span class="offer-price-text">{format_price(training.offer_price)}</span>'
                discount_html = f'<span class="badge badge-discount bg-success">{training.discount_percentage}% OFF</span>'
            else:
                offer_html = f'<span class="text-muted">{format_price(training.price)}</span>'
                discount_html = '<span class="badge badge-discount bg-secondary">No discount</span>'
            
            # Format created date
            created_html = training.created_at.strftime('%Y-%m-%d %H:%M')

            # Status badge
            status_badge = f'''
                <span class="badge bg-success rounded-pill">
                    <i class="fas fa-check-circle me-1"></i>Active
                </span>
            ''' if training.status else f'''
                <span class="badge bg-danger rounded-pill">
                    <i class="fas fa-times-circle me-1"></i>Inactive
                </span>
            '''
            
            # Status toggle button (separate from actions)
            status_button = status_badge
            if request.user.has_perm('trainings_app.change_training'):
                status_button = f'''
                    <button class="btn btn-sm status-toggle-btn {'btn-success' if training.status else 'btn-warning'}"
                            data-training-id="{training.pk}" 
                            data-status="{str(training.status).lower()}">
                        <i class="fas {'fa-check-circle' if training.status else 'fa-times-circle'} me-1"></i>
                        {'Active' if training.status else 'Inactive'}
                    </button>
                '''
            
            # Actions without status button
            actions_html = '<span class="text-muted">No actions</span>'
            
            # Check if user has edit or delete permissions
            can_edit = request.user.has_perm('trainings_app.change_training')
            can_delete = request.user.has_perm('trainings_app.delete_training')
            
            if can_edit or can_delete:
                actions_buttons = []
                
                if can_edit:
                    edit_url = reverse('trainings_app:training_edit', args=[training.pk])
                    images_url = reverse('trainings_app:training_images', args=[training.pk])
                    actions_buttons.append(
                        f'<a href="{edit_url}" class="btn btn-outline-primary btn-sm" '
                        f'data-bs-toggle="tooltip" title="Edit Training">'
                        f'<i class="fas fa-edit"></i></a>'
                    )
                    actions_buttons.append(
                        f'<a href="{images_url}" class="btn btn-outline-info btn-sm" '
                        f'data-bs-toggle="tooltip" title="Manage Images">'
                        f'<i class="fas fa-images"></i></a>'
                    )
                
                if can_delete:
                    delete_url = reverse('trainings_app:training_delete', args=[training.pk])
                    actions_buttons.append(
                        f'<a href="{delete_url}" class="btn btn-outline-danger btn-sm" '
                        f'onclick="return confirm(\'Are you sure you want to delete "{training.title}"?\')" '
                        f'data-bs-toggle="tooltip" title="Delete Training">'
                        f'<i class="fas fa-trash"></i></a>'
                    )
                
                actions_html = f'<div class="btn-group btn-group-sm" role="group">{"".join(actions_buttons)}</div>'
            
            data.append({
                'title': f'<strong>{training.title}</strong>',
                'image': image_html,
                'duration': f'<i class="fas fa-clock me-1"></i>{duration_display}',
                'description': description_html,
                'price': price_html,
                'offer_price': offer_html,
                'discount': discount_html,
                'status': status_button,
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
        logger.error(f"Error in trainings_datatables: {str(e)}")
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
        })

@rbac_permission_required('trainings_app.add_training')
def training_create(request):
    """Create new training"""
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save()
            messages.success(request, 'Training created successfully!')
            return redirect('trainings_app:training_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainingForm()
    
    context = {
        'form': form,
        'page_title': 'Create Training',
        'breadcrumb_active': 'Create Training'
    }
    return render(request, 'trainings/training_form.html', context)

@rbac_permission_required('trainings_app.change_training')
def training_edit(request, pk):
    """Edit existing training"""
    training = get_object_or_404(Training, pk=pk)
    
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, 'Training updated successfully!')
            return redirect('trainings_app:training_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TrainingForm(instance=training)
    
    context = {
        'form': form,
        'training': training,
        'page_title': 'Edit Training',
        'breadcrumb_active': 'Edit Training'
    }
    return render(request, 'trainings/training_form.html', context)

@rbac_permission_required('trainings_app.delete_training')
def training_delete(request, pk):
    """Delete training"""
    training = get_object_or_404(Training, pk=pk)
    
    if request.method == 'POST':
        training_name = training.title
        training.delete()
        messages.success(request, f'Training "{training_name}" deleted successfully!')
        return redirect('trainings_app:training_list')
    
    context = {
        'training': training,
        'page_title': 'Delete Training',
        'breadcrumb_active': 'Delete Training'
    }
    return render(request, 'trainings/training_confirm_delete.html', context)

@rbac_permission_required('trainings_app.change_training')
def training_images(request, pk):
    """Manage training images"""
    training = get_object_or_404(Training, pk=pk)
    
    if request.method == 'POST':
        # Handle multiple file uploads
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            start_order = int(request.POST.get('start_order', 0))
            auto_status = request.POST.get('auto_status') == 'true'
            
            try:
                for index, image_file in enumerate(images):
                    TrainingImage.objects.create(
                        training=training,
                        image=image_file,
                        order=start_order + index,
                        status=auto_status
                    )
                
                messages.success(request, f'{len(images)} images uploaded successfully!')
                return redirect('trainings_app:training_images', pk=training.pk)
                
            except Exception as e:
                messages.error(request, f'Error uploading images: {str(e)}')
        
        # Handle AJAX requests for TrainingImage operations
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return handle_training_image_ajax(request, training)
    
    formset = TrainingImageFormSet(instance=training)
    
    context = {
        'training': training,
        'formset': formset,
        'page_title': f'Manage Images - {training.title}',
        'breadcrumb_active': 'Training Images'
    }
    return render(request, 'trainings/training_images.html', context)

def handle_training_image_ajax(request, training):
    """Handle AJAX requests for TrainingImage operations"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        image_id = data.get('image_id')
        
        if action == 'update_order':
            new_order = data.get('order')
            return update_image_order(request, image_id, new_order)
        
        elif action == 'delete_image':
            return delete_image(request, image_id)
        
        elif action == 'toggle_image_status':
            return toggle_image_status(request, image_id)
            
        return JsonResponse({'success': False, 'error': 'Invalid action'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@rbac_permission_required('trainings_app.change_trainingimage')
def update_image_order(request, pk):
    """Update image order via AJAX"""
    if request.method == 'POST':
        try:
            image = get_object_or_404(TrainingImage, pk=pk)
            new_order = request.POST.get('order')
            image.order = new_order
            image.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@rbac_permission_required('trainings_app.delete_trainingimage')
def delete_image(request, pk):
    """Delete image via AJAX"""
    if request.method == 'POST':
        try:
            image = get_object_or_404(TrainingImage, pk=pk)
            image_name = str(image)
            image.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Image "{image_name}" deleted successfully!'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@rbac_permission_required('trainings_app.change_training')
def toggle_training_status(request, pk):
    """Toggle training status via AJAX"""
    if request.method == 'POST':
        try:
            training = get_object_or_404(Training, pk=pk)
            training.status = not training.status
            training.save()
            
            return JsonResponse({
                'success': True,
                'new_status': training.status,
                'message': f'Training status updated to {"Active" if training.status else "Inactive"}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@rbac_permission_required('trainings_app.change_trainingimage')
def toggle_image_status(request, pk):
    """Toggle image status via AJAX"""
    if request.method == 'POST':
        try:
            image = get_object_or_404(TrainingImage, pk=pk)
            image.status = not image.status
            image.save()
            
            return JsonResponse({
                'success': True,
                'new_status': image.status,
                'message': f'Image status updated to {"Active" if image.status else "Inactive"}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)