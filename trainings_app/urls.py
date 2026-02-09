from django.urls import path
from . import views

app_name = 'trainings_app'

urlpatterns = [
    path('trainings/', views.training_list, name='training_list'),
    path('datatables/', views.trainings_datatables, name='trainings_datatables'),
    path('create/', views.training_create, name='training_create'),
    path('edit/<int:pk>/', views.training_edit, name='training_edit'),


    path('delete/<int:pk>/', views.training_delete, name='training_delete'),
    path('images/<int:pk>/', views.training_images, name='training_images'),
    path('image/<int:pk>/toggle-status/', views.toggle_image_status, name='toggle_image_status'),
    path('toggle-status/<int:pk>/', views.toggle_training_status, name='toggle_training_status'),

    path('image/<int:pk>/toggle-status/', views.toggle_image_status, name='toggle_image_status'),  
    path('image/<int:pk>/update-order/', views.update_image_order, name='update_image_order'),
    path('image/<int:pk>/delete/', views.delete_image, name='delete_image'),
]