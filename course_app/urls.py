from django.urls import path
from . import views

app_name = 'course_app'

urlpatterns = [
    # Course URLs
    path('', views.courses_list, name='courses_list'),
    path('datatables/', views.courses_datatables, name='courses_datatables'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:pk>/toggle-status/', views.toggle_course_status, name='toggle_course_status'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enrollments/datatables/', views.course_enroll_datatable, name='course_enroll_datatable'),
    path('<int:pk>/course_enroll_delete/', views.course_enroll_delete, name='course_enroll_delete'),

    # Media CRUD URLs
    path('<int:pk>/media/', views.course_media_list, name='course_media_list'),
    path('<int:course_pk>/media/create/', views.media_create, name='media_create'),
    path('<int:course_pk>/media/<int:media_pk>/edit/', views.media_update, name='media_update'),
    path('<int:course_pk>/media/<int:media_pk>/delete/', views.media_delete, name='media_delete'),
    path('<int:course_pk>/media/<int:media_pk>/toggle-status/', views.toggle_media_status, name='toggle_media_status'),
]