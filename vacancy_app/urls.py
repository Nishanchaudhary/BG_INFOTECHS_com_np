from django.urls import path
from . import views

app_name = 'vacancy_app'

urlpatterns = [
    # Admin URLs
    path('', views.vacancy_list, name='vacancy_list'),
    path('datatables/', views.vacancies_datatables, name='vacancies_datatables'),
    path('create/', views.vacancy_create, name='vacancy_create'),
    path('edit/<int:pk>/', views.vacancy_edit, name='vacancy_edit'),
    path('delete/<int:pk>/', views.vacancy_delete, name='vacancy_delete'),
    path('toggle-status/<int:pk>/', views.toggle_vacancy_status, name='toggle_vacancy_status'),
    # Public URLs
    path('<int:pk>/', views.vacancy_detail, name='vacancy_detail'),

     # Job Application URLs
    path('applications/', views.application_list, name='application_list'),
    path('applications/datatables/', views.application_datatables, name='application_datatables'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/edit/<int:pk>/', views.application_edit, name='application_edit'),
    path('applications/create/<int:vacancy_pk>/', views.application_create, name='application_create_for_vacancy'),
    path('applications/delete/<int:pk>/', views.application_delete, name='application_delete'),
    # path('applications/update-status/', views.update_application_status, name='update_application_status'),
    path('applications/toggle-status/<int:pk>/', views.toggle_application_status, name='toggle_application_status'),

]