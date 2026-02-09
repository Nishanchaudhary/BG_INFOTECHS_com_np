from django.urls import path
from . import views

app_name = 'teams_app'

urlpatterns = [
    # Admin URLs
    path('', views.teams_list, name='teams_list'),
    path('datatables/', views.teams_datatables, name='teams_datatables'),
    path('create/', views.team_create, name='team_create'),
    path('edit/<int:pk>/', views.team_edit, name='team_edit'),
    path('delete/<int:pk>/', views.team_delete, name='team_delete'),
    path('toggle-status/<int:pk>/', views.toggle_team_status, name='toggle_team_status'),

    # New Features
    # path('bulk-management/', views.bulk_team_management, name='bulk_team_management'),
    # path('statistics/', views.team_statistics, name='team_statistics'),
    # path('profile/<int:pk>/', views.team_profile, name='team_profile'),
]