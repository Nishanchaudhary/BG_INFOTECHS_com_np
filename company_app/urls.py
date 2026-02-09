from . import views
from django.urls import path

app_name = 'company_app'

urlpatterns = [
    path('company/profile/', views.company_profile_view, name='company_profile'),
    # Features URLs
    path('features/create/', views.feature_create, name='feature_create'),
    path('features/', views.feature_list, name='feature_list'), 
    path('features/api/', views.features_datatables_api, name='features_datatables_api'),  # NEW
    path('features/edit/<int:pk>/', views.feature_edit, name='feature_edit'),
    path('features/delete/<int:pk>/', views.feature_delete, name='feature_delete'),
    
    # Services URLs
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.services_create, name='services_create'),
    path('services/details/<int:pk>/', views.service_details, name='service_details'),
    path('services/edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('services/delete/<int:pk>/', views.service_delete, name='service_delete'),
    path('services/datatables/', views.services_datatables_api, name='services_datatables_api'),

    # Services Success URLs
    path('services-success/', views.services_success_list, name='services_success_list'),
    path('services-success/api/', views.services_success_datatables_api, name='services_success_datatables_api'),
    path('services-success/create/', views.services_success_create, name='services_success_create'),
    path('services-success/<int:pk>/', views.services_success_details, name='services_success_details'),
    path('services-success/<int:pk>/edit/', views.services_success_edit, name='services_success_edit'),
    path('services-success/<int:pk>/delete/', views.services_success_delete, name='services_success_delete'),

    # Testimonials URLs
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/datatables/', views.testimonial_datatables_api, name='testimonial_datatables_api'),
    path('testimonials/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonials/edit/<int:pk>/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/delete/<int:pk>/', views.testimonial_delete, name='testimonial_delete'),

    # Projects Done URLs
    path('projects-done/', views.project_done_list, name='project_done_list'),
    path('projects-done/datatables/', views.project_done_datatables_api, name='project_done_datatables_api'),
    path('projects-done/create/', views.project_done_create, name='project_done_create'),
    path('projects-done/edit/<int:pk>/', views.project_done_edit, name='project_done_edit'),
    path('projects-done/delete/<int:pk>/', views.project_done_delete, name='project_done_delete'),

# Services Testimonials URLs
    path('services-testimonials/', views.services_testimonial_list, name='services_testimonial_list'),
    path('services-testimonials/datatables/', views.services_testimonial_datatables_api, name='services_testimonial_datatables_api'),
    path('services-testimonials/create/', views.services_testimonial_create, name='services_testimonial_create'),
    path('services-testimonials/edit/<int:pk>/', views.services_testimonial_edit, name='services_testimonial_edit'),
    path('services-testimonials/delete/<int:pk>/', views.services_testimonial_delete, name='services_testimonial_delete'),
    path('services-testimonials/<int:pk>/', views.services_testimonial_detail, name='services_testimonial_detail'),
    path('services-testimonials/toggle-status/<int:pk>/', views.toggle_services_testimonial_status, name='toggle_services_testimonial_status'),

     # Services FAQs URLs
    path('services-faqs/', views.services_faq_list, name='services_faq_list'),
    path('services/<int:service_id>/faqs/', views.service_faqs_list, name='service_faqs_list'),
    path('services-faqs/datatables/', views.services_faq_datatables_api, name='services_faq_datatables_api'),
    path('services-faqs/create/', views.services_faq_create, name='services_faq_create'),
    path('services-faqs/edit/<int:pk>/', views.services_faq_edit, name='services_faq_edit'),
    path('services-faqs/delete/<int:pk>/', views.services_faq_delete, name='services_faq_delete'),
    path('services-faqs/detail/<int:pk>/', views.services_faq_detail, name='services_faq_detail'),
    path('services-faq/<int:pk>/toggle-status/', views.toggle_services_faq_status, name='toggle_services_faq_status'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/datatables/', views.category_datatables_api, name='category_datatables_api'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

]