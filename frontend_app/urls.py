from django.urls import path
from django.conf import settings
from . import views

app_name = 'frontend_app' 

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('search-engine-optimization/', views.seo, name='search_engine_optimization'),
    path('all_seo/', views.all_seo, name='all_seo'),
    path('mobile-apps/', views.mobile_app, name='mobile_apps'),
    path('all-mobile-apps/', views.all_mobile_apps, name='all_mobile_apps'),
    path('web_development/', views.web_development, name='web_development'),
    path('all_web_development/', views.all_web_development, name='all_web_development'),
    path('graphic_designing/', views.graphic, name='graphic_designing'),
    path('all_graphic_design/', views.all_graphic_design, name='all_graphic_design'),
    path('social_media_marketing/', views.smm, name='social_media_marketing'),
    path('digital_marketing/', views.digital_marketing, name='digital_marketing'),
    path('all_digital_marketing', views.all_digital_marketing, name='all_digital_marketing'),

    path('training/', views.training, name='training'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('enroll/course/<int:pk>/', views.enroll_course, name='enroll_course'),
    path('enroll/process/<int:pk>/', views.process_enrollment, name='process_enrollment'),

    path('features/', views.features, name='features'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/list/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_details, name='blog_details'),
    path('career/', views.careers, name='career'),
    path('all_careers/', views.all_careers, name='all_careers'),
    path('careers/<int:pk>/', views.career_details, name='career_details'), 
    path('my-applications/', views.my_applications, name='my_applications'),
    path('contact/', views.contact, name='contact'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]

urlpatterns += [
    path('<path:undefined_path>/', views.handler404_override),
]