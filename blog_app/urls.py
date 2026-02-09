from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # Blog management URLs
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/datatables/', views.blogs_datatables, name='blogs_datatables'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blogs/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('blogs/<int:pk>/toggle-status/', views.toggle_blog_status, name='toggle_blog_status'),
    path('blogs/<int:pk>/comments/', views.blog_comments, name='blog_comments'),
    path('blogs/<int:pk>/comments/<int:comment_id>/delete/', views.blog_comments_delete, name='blog_comments_delete'),
    
    # Category URLs - MUST come before the slug pattern
    path('categories/', views.category_list, name='category_list'),
    path('categories/datatables/', views.categories_datatables, name='categories_datatables'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # AJAX endpoints
    path('ajax/comment-action/', views.ajax_comment_action, name='ajax_comment_action'),
    
    # Public blog detail - MUST be LAST to avoid catching other URLs
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]