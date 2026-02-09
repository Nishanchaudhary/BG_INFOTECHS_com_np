from . import views
from django.urls import path

app_name = 'package_app'

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('packages/datatables/', views.package_datatables_api, name='package_datatables_api'),
    path('packages/create/', views.package_create, name='package_create'),
    path('packages/edit/<int:pk>/', views.package_edit, name='package_edit'),
    path('packages/delete/<int:pk>/', views.package_delete, name='package_delete'),

    # plansubscriber
    path('planSubscriber-list/', views.planSubscriber_list, name='planSubscriber_list'),
    path('planSubscriber_datatable_api/', views.planSubscriber_datatable_api, name='planSubscriber_datatable_api'),
    path('planSubscriber_delete/<int:pk>/', views.planSubscriber_delete, name='planSubscriber_delete'),

    # Custom Package URLs
    path('custom-packages/', views.custom_package_list, name='custom_package_list'),
    path('custom-packages/datatables/', views.custom_package_datatables_api, name='custom_package_datatables_api'),
    path('custom-packages/delete/<int:pk>/', views.custom_package_delete, name='custom_package_delete'),    
]