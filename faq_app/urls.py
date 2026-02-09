from django.urls import path
from . import views

app_name = 'faq_app'

urlpatterns = [

    # Slider URLs
    path('sliders/', views.slider_list, name='slider_list'),
    path('sliders/datatables/', views.sliders_datatables, name='sliders_datatables'),
    path('sliders/create/', views.slider_create, name='slider_create'),
    path('sliders/edit/<int:pk>/', views.slider_edit, name='slider_edit'),
    path('sliders/delete/<int:pk>/', views.slider_delete, name='slider_delete'),
    path('sliders/toggle-status/<int:pk>/', views.toggle_slider_status, name='toggle_slider_status'),
    path('sliders/<int:pk>/', views.slider_detail, name='slider_detail'),
    path('sliders/active/', views.active_sliders, name='active_sliders'),


    path('', views.faq_list, name='faq_list'),
    path('datatables/', views.faqs_datatables, name='faqs_datatables'),
    path('create/', views.faq_create, name='faq_create'),
    path('edit/<int:pk>/', views.faq_edit, name='faq_edit'),
    path('delete/<int:pk>/', views.faq_delete, name='faq_delete'),
    path('toggle-status/<int:pk>/', views.toggle_faq_status, name='toggle_faq_status'),
    path('<slug:slug>/', views.faq_detail, name='faq_detail'),

    
]