# bg_app/urls.py
from django.urls import path, include
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

app_name = 'bg_app'

urlpatterns = [
    # =========================================================================
    # AUTHENTICATION URLS
    # =========================================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # =========================================================================
    # PASSWORD RESET URLS
    # =========================================================================
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    
    # =========================================================================
    # DASHBOARD URLS
    # =========================================================================
    path('', lambda request: redirect('bg_app:login'), name='home'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # =========================================================================
    # ROLE MANAGEMENT URLS
    # =========================================================================
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/edit/<int:role_id>/', views.role_edit, name='role_edit'),
    path('roles/delete/<int:role_id>/', views.role_delete, name='role_delete'),
    
    # =========================================================================
    # Staff Permissions Management
    # ========================================================================= 
    path('staff/permissions/', views.staff_permissions, name='staff_permissions'),
    path('staff/<int:user_id>/permissions/', views.edit_staff_permissions, name='edit_staff_permissions'),
    path('api/staff-datatables/', views.staff_datatables_api, name='staff_datatables_api'),
    path('staff/<int:user_id>/toggle-status/', views.toggle_staff_status, name='toggle_staff_status'),
    
    # User Permissions Management
    path('users/<int:user_id>/permissions/', views.user_permissions, name='user_permissions'),
    path('users/<int:user_id>/permission-summary/', views.permission_summary, name='permission_summary'),
    
    # =========================================================================
    # USER MANAGEMENT URLS
    # =========================================================================
    path('users/', views.user_list, name='user_list'),
    path('users/api/', views.user_datatables_api, name='user_datatables_api'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:pk>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),

    # =========================================================================
    # PROFILE MANAGEMENT URLS
    # =========================================================================
    # Student Profile Management
    path('users/<int:user_id>/create-student/', views.create_student, name='create_student'),
    path('users/<int:user_id>/edit-student/', views.edit_student, name='edit_student'),
    path('users/<int:user_id>/update-fees/', views.update_student_fees, name='update_student_fees'),
    
    # Staff Profile Management
    path('users/<int:user_id>/create-staff/', views.create_staff, name='create_staff'),
    path('users/<int:user_id>/edit-staff/', views.edit_staff, name='edit_staff'),
    path('users/<int:user_id>/update-salary/', views.update_staff_salary, name='update_staff_salary'),
    
    # =========================================================================
    # DJANGO PERMISSION MANAGEMENT URLS
    # =========================================================================
    path('custom-admin/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('users/<int:user_id>/save-permissions/', views.save_user_permissions, name='save_user_permissions'),
    path('users/<int:user_id>/save-groups/', views.save_user_groups, name='save_groups'),
]

# =============================================================================
# URL PATTERNS FOR API ENDPOINTS (Optional - for frontend integration)
# =============================================================================

api_urlpatterns = [
    # Role API endpoints
    path('api/roles/', views.role_list, name='api_role_list'),
    path('api/roles/create/', views.role_create, name='api_role_create'),
    path('api/roles/<int:role_id>/edit/', views.role_edit, name='api_role_edit'),
    path('api/roles/<int:role_id>/delete/', views.role_delete, name='api_role_delete'),
    
    # Permission API endpoints
    path('api/staff/permissions/', views.staff_permissions, name='api_staff_permissions'),
    path('api/staff/<int:user_id>/permissions/', views.edit_staff_permissions, name='api_edit_staff_permissions'),
    path('api/staff/<int:user_id>/toggle-status/', views.toggle_staff_status, name='api_toggle_staff_status'),
    
    # User API endpoints
    path('api/users/', views.user_datatables_api, name='api_user_list'),
    path('api/users/<int:user_id>/permissions/', views.user_permissions, name='api_user_permissions'),
]

# Include API URLs if needed
# urlpatterns += api_urlpatterns