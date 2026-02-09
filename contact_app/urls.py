from . import views
from django.urls import path

app_name = 'contact_app'

urlpatterns = [
    path('', views.branch_list, name='branch_list'),
    path('branches/datatables/', views.branch_datatables_api, name='branch_datatables_api'),
    path('branches/create/', views.branch_create, name='branch_create'),
    path('branches/edit/<int:pk>/', views.branch_edit, name='branch_edit'),
    path('branches/delete/<int:pk>/', views.branch_delete, name='branch_delete'),

    # contact.....................................................
    path('contact-list', views.contact_list, name='contact_list'),
    path('contact-datatable_api', views.contact_datatable_api, name='contact_datatable_api'),
    path('contact-mark-read', views.contact_mark_read, name='contact_mark_read'),
    path('contact-mark-unread', views.contact_mark_unread, name='contact_mark_unread'),
    path('contact-delete', views.contact_delete, name='contact_delete')
]