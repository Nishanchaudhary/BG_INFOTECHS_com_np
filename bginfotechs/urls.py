"""
URL configuration for bginfotechs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('bg_app/', include('bg_app.urls')),
    path('company_app/', include('company_app.urls')),
    path('trainings_app/', include('trainings_app.urls',)),
    path('blog_app/', include('blog_app.urls')),
    path('vacancy_app/', include('vacancy_app.urls')),
    path('teams_app/', include('teams_app.urls')),
    path('faq_app/', include('faq_app.urls')),
    path('course_app/', include(('course_app.urls', 'course_app'), namespace='course_app')),
    path('package_app/', include('package_app.urls')),
    path('contact_app/', include('contact_app.urls')),
    

    # Frontend url ...................
    path('', include('frontend_app.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'frontend_app.views.handler404'