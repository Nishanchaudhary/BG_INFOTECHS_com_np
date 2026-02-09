from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from blog_app.models import Blog, BlogComment, Category
from company_app.models import Company_profile, Features, Services, Testimonials, Project_done, Services_testimonial, Services_faq,Services_success
from course_app.models import Course, Media,CourseEnrollment
from faq_app.models import FAQ, Slider
from django.contrib import messages
from package_app.models import Package,PlanSubscriber,CustomPackage
from teams_app.models import Teams
from trainings_app.models import Training, TrainingImage
from vacancy_app.models import Vacancy, JobApplication
from vacancy_app.forms import JobApplicationForm
from contact_app.models import Branch,Contact
from django.core.mail import send_mail
from django.conf import settings
from course_app.forms import CourseEnrollmentForm
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from .forms import PlanSubscriberForm, CustomPackageForm,ContactForm
from django.db.models import Count as CountFunc

# Home Page View..........................................................................
def home(request):
    features = Features.objects.filter(status=True)[:6]
    services = Services.objects.filter(status=True)[:6]

    services_with_success = []
    for service in services:
        service_success_items = Services_success.objects.filter(
            status=True, 
            service=service
        )[:3]  
        services_with_success.append({
            'service': service,
            'success_items': service_success_items
        })

    testimonials = Testimonials.objects.filter(status=True)
    company_profile = Company_profile.objects.first()
    latest_blogs = Blog.objects.filter(status='published').order_by('-created_at')[:3]
    
    context = {
        'features': features,
        'services': services,
        'services_with_success': services_with_success,  # Updated this
        'testimonials': testimonials,
        'company_profile': company_profile,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'Frontend/index.html', context)

# About Page View.....................................................................
def about(request):
    company_profile = Company_profile.objects.first()
    team_members = Teams.objects.filter(status='active').order_by('display_order')
    testimonials = Testimonials.objects.filter(status=True)
    first_vacancy = Vacancy.objects.filter(status='active').first()
    context = {
        'company_profile': company_profile,
        'team_members': team_members,
        'testimonials': testimonials,
        'first_vacancy': first_vacancy,
    }
    return render(request, 'Frontend/about.html', context)

# Services Page View.....................................................................
def services(request):
    all_services = Services.objects.filter(status=True)
    service_testimonials = Services_testimonial.objects.filter(status=True)
    service_faqs = Services_faq.objects.filter(status='published')
    
    context = {
        'services': all_services,
        'service_testimonials': service_testimonials,
        'service_faqs': service_faqs,
    }
    return render(request, 'Frontend/services.html', context)

from company_app.models import Category

# ===============================================================================
# Web Development Page View
# ===============================================================================

def web_development(request):
    try:
        web_keywords = [
            'web development', 'web', 'web app development', 'website development',
            'web application development', 'websites', 'full stack', 'frontend', 
            'backend', 'ecommerce', 'responsive', 'web design', 'web application'
        ]
        
        # Build dynamic Q object
        q_objects = Q()
        for keyword in web_keywords:
            q_objects |= Q(title__icontains=keyword)
        
        service = Services.objects.filter(
            q_objects,
            status=True
        ).first()
        
        if not service:
            service = Services.objects.filter(status=True).first()
            if not service:
                service = Services.objects.create(
                    title='Web Development',
                    sub_title='Professional Web Development Services',
                    description='We provide comprehensive web development solutions including custom web applications, e-commerce platforms, and responsive websites.',
                    status=True
                )
        
        # Get related projects (equivalent to recent_projects in original)
        related_projects = Project_done.objects.filter(service=service, status=True)
        
        # Get projects with logos
        related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)
        
        # Get categories based on web-related keywords
        categories = Category.objects.filter(
            Q(title__icontains='web') |
            Q(title__icontains='development') |
            Q(title__icontains='application') |
            Q(title__icontains='website') |
            Q(title__icontains='full stack') |
            Q(title__icontains='frontend') |
            Q(title__icontains='backend'),
            status=True
        ).distinct()
        
        if not categories:
            categories = Category.objects.filter(status=True).distinct()
        
        # Get service testimonials and FAQs
        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)
        service_faqs = Services_faq.objects.filter(service=service, status='published')
        
        # Get company profile
        company_profile = Company_profile.objects.first()
        
        context = {
            'service': service,
            'related_projects': related_projects,
            'related_projects_logo': related_projects_logo,
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
            'company_profile': company_profile,
        }
        
        return render(request, 'Frontend/web-development.html', context)
    
    except Exception as e:
        print(f"Error in web_development view: {str(e)}")
        return render(request, 'Frontend/web-development.html', {
            'service': None,
            'related_projects': [],
            'related_projects_logo': [],
            'categories': [],
            'service_testimonials': [],
            'service_faqs': [],
            'company_profile': None,
        })
    
def all_web_development(request):
    # Get web development category
    try:
        web_dev_category = Category.objects.get(title__icontains='web development', status=True)
    except Category.DoesNotExist:
        # Fallback: get first active category or all projects
        web_dev_category = Category.objects.filter(status=True).first()
    
    # Get all projects, filter by web development category if available
    if web_dev_category:
        projects = Project_done.objects.filter(
            status=True, 
            category=web_dev_category
        ).order_by('-created_at')
    else:
        projects = Project_done.objects.filter(status=True).order_by('-created_at')
    
    # Get all categories for filter dropdown
    categories = Category.objects.filter(status=True)
    
    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Handle category filter
    category_filter = request.GET.get('category', '')
    active_category = None
    if category_filter:
        try:
            active_category = Category.objects.get(id=category_filter, status=True)
            projects = projects.filter(category=active_category)
        except Category.DoesNotExist:
            pass
    
    # Get project counts for each category
    category_counts = {}
    for category in categories:
        count = Project_done.objects.filter(
            status=True, 
            category=category
        ).count()
        category_counts[category.id] = count
    
    # Get web development category count
    web_dev_count = 0
    if web_dev_category:
        web_dev_count = Project_done.objects.filter(
            status=True, 
            category=web_dev_category
        ).count()
    
    # Get total project count
    total_projects = projects.count()
    
    # Pagination - 6 projects per page
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'search_query': search_query,
        'categories': categories,
        'category_filter': category_filter,
        'active_category': active_category,
        'category_counts': category_counts,
        'total_projects': total_projects,
        'web_dev_category': web_dev_category,
        'web_dev_count': web_dev_count,
    }

    return render(request, 'Frontend/all_web_development.html', context)

# ===============================================================================
# Graphic Designing Page View
# ===============================================================================

def graphic(request):
    try:
        graphic_keywords = [
            'graphic', 'design', 'branding', 'packaging', 
            'logo', 'print', 'ui', 'ux', 'social media'
        ]
        
        # Build dynamic Q object
        q_objects = Q()
        for keyword in graphic_keywords:
            q_objects |= Q(title__icontains=keyword)
        
        service = Services.objects.filter(
            q_objects,
            status=True
        ).first()
        
        if not service:
            service = Services.objects.filter(status=True).first()
            if not service:
                service = Services.objects.create(
                    title='Graphic Design',
                    sub_title='Professional Graphic Design Services',
                    description='We provide comprehensive graphic design solutions including logo design, branding, and marketing materials.',
                    status=True
                )
        
        related_projects = Project_done.objects.filter(service=service, status=True)
        
        related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)
        
        categories = Category.objects.filter(
            project_done__service=service,
            project_done__status=True,
            status=True
        ).distinct()
        
        if not categories:
            categories = Category.objects.filter(status=True).distinct()
        
        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)
        service_faqs = Services_faq.objects.filter(service=service, status='published')
        
        context = {
            'service': service,
            'related_projects': related_projects,
            'related_projects_logo': related_projects_logo,
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
        }
        
        return render(request, 'Frontend/graphic_designing.html', context)
    
    except Exception as e:
        print(f"Error in graphic view: {str(e)}")
        return render(request, 'Frontend/graphic_designing.html', {
            'service': None,
            'related_projects': [],
            'related_projects_logo': [],
            'categories': [],
            'service_testimonials': [],
            'service_faqs': [],
        })

def all_graphic_design(request):
    try:
        graphic_keywords = [
            'graphic', 'design', 'branding', 'packaging', 
            'logo', 'print', 'ui', 'ux', 'social media'
        ]
        q_objects = Q()
        for keyword in graphic_keywords:
            q_objects |= Q(title__icontains=keyword)

        service = Services.objects.filter(
            q_objects,
            status=True
        ).first()

        if not service:
            service = Services.objects.filter(status=True).first()

        # Use a queryset variable for pagination and for category calculations
        if service:
            related_projects_qs = Project_done.objects.filter(
                service=service,
                status=True
            ).select_related('category', 'service').order_by('-created_at')
        else:
            related_projects_qs = Project_done.objects.filter(
                status=True
            ).select_related('category', 'service').order_by('-created_at')

        # Categories should be derived from the full queryset (not just the page)
        categories = Category.objects.filter(
            project_done__in=related_projects_qs,
            status=True
        ).distinct()

        if service:
            service_testimonials = Services_testimonial.objects.filter(
                service=service,
                status=True
            )
            service_faqs = Services_faq.objects.filter(
                service=service,
                status='published'
            )
        else:
            service_testimonials = Services_testimonial.objects.filter(status=True)
            service_faqs = Services_faq.objects.filter(status='published')

        # Pagination: change page_size as needed
        page_size = 6
        paginator = Paginator(related_projects_qs, page_size)
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'service': service,
            'related_projects': page_obj,          # Page object for template
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': page_obj.has_other_pages(),
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
        }

        return render(request, 'Frontend/all_graphic_design.html', context)

    except Exception as e:
        print(f"Error in all_graphic_design view: {str(e)}")
        return render(request, 'Frontend/all_graphic_design.html', {
            'service': None,
            'related_projects': Project_done.objects.none(),
            'categories': Category.objects.none(),
            'service_testimonials': Services_testimonial.objects.none(),
            'service_faqs': Services_faq.objects.none(),
            'page_obj': None,
            'paginator': None,
            'is_paginated': False,
        })

# ===============================================================================
# SEO Page View 
# ===============================================================================
def seo(request):
    try:
        seo_keywords = [
            'seo', 'search engine', 'search engine optimization', 'on-page', 'off-page',
            'technical seo', 'keyword', 'link building', 'organic', 'rank'
        ]
        q_objects = Q()
        for kw in seo_keywords:
            q_objects |= Q(title__icontains=kw)

        service = Services.objects.filter(q_objects, status=True).first()
        if not service:
            service, _ = Services.objects.get_or_create(
                title='SEO Services',
                defaults={
                    'sub_title': 'Professional SEO Services',
                    'description': 'We provide comprehensive SEO: on-page, off-page and technical SEO to boost organic visibility.',
                    'status': True
                }
            )

        # Get related projects (all projects for this service)
        related_projects = Project_done.objects.filter(service=service, status=True)
        
        # Apply the logo feature from graphic view
        related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)
        
        # If no recent projects with this service, fallback to SEO-related projects
        if not related_projects:
            related_projects = Project_done.objects.filter(
                Q(title__icontains='seo') | Q(description__icontains='seo'),
                status=True
            ).select_related('service', 'category').order_by('-created_at')[:6]
            # Also update the logo projects with the fallback
            related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)

        categories = Category.objects.filter(
            project_done__service=service,
            project_done__status=True,
            status=True
        ).distinct()
        if not categories.exists():
            categories = Category.objects.filter(status=True).distinct()[:6]

        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)[:3]
        service_faqs = Services_faq.objects.filter(service=service, status='published')[:5]
        company_profile = Company_profile.objects.first()

        context = {
            'service': service,
            'related_projects': related_projects,  # Changed from recent_projects to match graphic view
            'related_projects_logo': related_projects_logo,  # Added logo feature
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
            'company_profile': company_profile,
        }
        return render(request, 'Frontend/seo.html', context)

    except Exception as e:
        print(f"Error in seo view: {e}")
        return render(request, 'Frontend/seo.html', {
            'service': None,
            'related_projects': [],  # Updated variable name
            'related_projects_logo': [],  # Added to error context
            'categories': [],
            'service_testimonials': [],
            'service_faqs': [],
            'company_profile': None,
        })
    
def all_seo(request):
    try:
        # SEO keywords for filtering (same as seo view)
        seo_keywords = [
            'seo', 'search engine', 'search engine optimization', 'on-page', 'off-page',
            'technical seo', 'keyword', 'link building', 'organic', 'rank'
        ]
        
        # Build Q objects for SEO filtering (same logic as seo view)
        q_objects = Q()
        for kw in seo_keywords:
            q_objects |= Q(title__icontains=kw)
        
        # Get SEO service using the same filtering method
        seo_service = Services.objects.filter(q_objects, status=True).first()
        
        # If no SEO service found, create a default one (same as seo view)
        if not seo_service:
            seo_service, _ = Services.objects.get_or_create(
                title='SEO Services',
                defaults={
                    'sub_title': 'Professional SEO Services',
                    'description': 'We provide comprehensive SEO: on-page, off-page and technical SEO to boost organic visibility.',
                    'status': True
                }
            )
        
        # Get all projects related to SEO service (same as seo view but all projects)
        projects = Project_done.objects.filter(service=seo_service, status=True)
        
        # Apply logo feature (same as seo view)
        projects_logo = projects.exclude(logo='').exclude(logo__isnull=True)
        
        # If no projects with SEO service, fallback to SEO-related projects (same logic)
        if not projects:
            projects = Project_done.objects.filter(
                Q(title__icontains='seo') | Q(description__icontains='seo'),
                status=True
            ).select_related('service', 'category').order_by('-created_at')
            # Also update logo projects with fallback
            projects_logo = projects.exclude(logo='').exclude(logo__isnull=True)
        
        # Get categories (same logic as seo view)
        categories = Category.objects.filter(
            project_done__service=seo_service,
            project_done__status=True,
            status=True
        ).distinct()
        
        if not categories.exists():
            categories = Category.objects.filter(status=True).distinct()
        
        # Handle search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Handle category filter
        category_filter = request.GET.get('category', '')
        active_category = None
        if category_filter:
            try:
                active_category = Category.objects.get(id=category_filter, status=True)
                projects = projects.filter(category=active_category)
            except Category.DoesNotExist:
                pass
        
        # Get project counts for each category
        category_counts = {}
        for category in categories:
            count = Project_done.objects.filter(
                status=True, 
                category=category,
                service=seo_service  # Only count projects for SEO service
            ).count()
            category_counts[category.id] = count
        
        # Get total project count
        total_projects = projects.count()
        
        # Pagination - 6 projects per page
        paginator = Paginator(projects, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get testimonials for SEO (same as seo view)
        service_testimonials = Services_testimonial.objects.filter(service=seo_service, status=True)[:3]
        
        # Company profile (same as seo view)
        company_profile = Company_profile.objects.first()
        
        context = {
            'projects': page_obj,
            'projects_logo': projects_logo,  # Same variable name as seo view
            'search_query': search_query,
            'categories': categories,
            'category_filter': category_filter,
            'active_category': active_category,
            'category_counts': category_counts,
            'total_projects': total_projects,
            'seo_service': seo_service,  # Same variable name as seo view
            'service_testimonials': service_testimonials,  # Same variable name
            'company_profile': company_profile,  # Same variable name
        }
        
        return render(request, 'Frontend/all_seo.html', context)
        
    except Exception as e:
        print(f"Error in all_seo view: {e}")
        return render(request, 'Frontend/all_seo.html', {
            'projects': [],
            'projects_logo': [],
            'search_query': '',
            'categories': [],
            'category_filter': '',
            'active_category': None,
            'category_counts': {},
            'total_projects': 0,
            'seo_service': None,
            'service_testimonials': [],
            'company_profile': None,
        })
    
# ===============================================================================
# mobile_apps Page View 
# ===============================================================================
def mobile_app(request):
    try:
        mobile_keywords = [
            'mobile app', 'mobile application', 'ios', 'android', 'react native',
            'flutter', 'cross platform', 'hybrid app', 'app development'
        ]
        
        # Build dynamic Q object
        q_objects = Q()
        for keyword in mobile_keywords:
            q_objects |= Q(title__icontains=keyword)
        
        service = Services.objects.filter(
            q_objects,
            status=True
        ).first()
        
        if not service:
            service = Services.objects.filter(status=True).first()
            if not service:
                service = Services.objects.create(
                    title='Mobile App Development',
                    sub_title='Professional Mobile App Development Services',
                    description='We provide comprehensive mobile app development solutions including native iOS, native Android, and cross-platform applications using modern technologies.',
                    status=True
                )
        
        # Get related projects
        related_projects = Project_done.objects.filter(service=service, status=True)
        
        # Apply logo filtering from graphic view
        related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)
        
        # Fallback if no projects found for mobile service
        if not related_projects:
            related_projects = Project_done.objects.filter(
                Q(title__icontains='app') |
                Q(title__icontains='mobile') |
                Q(title__icontains='ios') |
                Q(title__icontains='android'),
                status=True
            ).select_related('service', 'category').order_by('-created_at')[:6]
            # Also update logo projects with fallback
            related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)
        
        # Get categories using graphic view logic
        categories = Category.objects.filter(
            project_done__service=service,
            project_done__status=True,
            status=True
        ).distinct()
        
        if not categories:
            # Fallback to mobile-specific categories
            category_fields = [f.name for f in Category._meta.get_fields()]
            if 'title' in category_fields:
                categories = Category.objects.filter(
                    Q(title__icontains='mobile') |
                    Q(title__icontains='app') |
                    Q(title__icontains='ios') |
                    Q(title__icontains='android') |
                    Q(title__icontains='react native') |
                    Q(title__icontains='flutter') |
                    Q(title__icontains='cross platform'),
                    status=True
                )[:6]
            else:
                categories = Category.objects.filter(status=True).distinct()
        
        # Get service testimonials and FAQs
        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)
        service_faqs = Services_faq.objects.filter(service=service, status='published')
        
        company_profile = Company_profile.objects.first()

        context = {
            'service': service,
            'related_projects': related_projects,
            'related_projects_logo': related_projects_logo,
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
            'company_profile': company_profile,
        }
        return render(request, 'Frontend/mobile-apps.html', context)
    
    except Exception as e:
        print(f"Error in mobile_app view: {str(e)}")
        return render(request, 'Frontend/mobile-apps.html', {
            'service': None,
            'related_projects': [],
            'related_projects_logo': [],
            'categories': [],
            'service_testimonials': [],
            'service_faqs': [],
            'company_profile': None,
        })

def all_mobile_apps(request):
    try:
        # Query for mobile app related service
        service = Services.objects.filter(
            Q(title__icontains='Mobile App') | 
            Q(title__icontains='Mobile Application') |
            Q(title__icontains='iOS') |
            Q(title__icontains='Android') |
            Q(title__icontains='React Native') |
            Q(title__icontains='Flutter'),
            status=True
        ).first()
        
        # If no mobile app service found, create a default one
        if not service:
            service, created = Services.objects.get_or_create(
                title='Mobile App Development',
                defaults={
                    'sub_title': 'Professional Mobile App Development Services',
                    'description': 'We provide comprehensive mobile app development solutions.',
                    'status': True
                }
            )

        # Get all mobile projects with pagination or filtering
        mobile_projects = Project_done.objects.filter(
            Q(service=service) |
            Q(title__icontains='app') |
            Q(title__icontains='mobile') |
            Q(title__icontains='iOS') |
            Q(title__icontains='Android') |
            Q(description__icontains='mobile app') |
            Q(description__icontains='iOS') |
            Q(description__icontains='Android'),
            status=True
        ).select_related('service', 'category').order_by('-created_at')

        # Get mobile-related categories for filtering
        mobile_categories = Category.objects.filter(
            Q(title__icontains='mobile') |
            Q(title__icontains='app') |
            Q(title__icontains='iOS') |
            Q(title__icontains='Android'),
            status=True
        )
        company_profile = Company_profile.objects.first()

        context = {
            'service': service,
            'mobile_projects': mobile_projects,
            'mobile_categories': mobile_categories,
            'company_profile': company_profile,
        }
        return render(request, 'Frontend/all_mobile_apps.html', context)
    
    except Exception as e:
        print(f"Error in all_mobile_apps view: {e}")
        context = {
            'service': None,
            'mobile_projects': [],
            'mobile_categories': [],
        }
        return render(request, 'Frontend/all_mobile_apps.html', context)
# ===============================================================================
# Social Media Marketing Page View 
# ===============================================================================
def smm(request):
    try:
        # Service keywords for SMM
        service_keywords = [
            'social', 'smm', 'social media', 'media marketing', 'social media marketing',
            'facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok',
            'content creation', 'influencer', 'community management', 'social advertising'
        ]
        
        # Build dynamic Q object for service
        q_service = Q()
        for keyword in service_keywords:
            q_service |= Q(title__icontains=keyword)

        # Find matching service
        service = Services.objects.filter(
            q_service,
            status=True
        ).first()
        
        # Fallback: get any active service or create default
        if not service:
            service = Services.objects.filter(status=True).first()
            if not service:
                service = Services.objects.create(
                    title='Social Media Marketing',
                    sub_title='Professional Social Media Marketing Services',
                    description='We provide comprehensive social media marketing solutions including content creation, community management, influencer collaborations, and paid social advertising across all major platforms.',
                    status=True
                )

        # Get related projects for this service with LIMIT of 4
        related_projects = Project_done.objects.filter(service=service, status=True).order_by('-created_at')[:4]
        
        # Get projects with logos (for logo showcase) - also limited to 4
        related_projects_logo = Project_done.objects.filter(
            service=service, 
            status=True
        ).exclude(logo__exact='').exclude(logo__isnull=True).order_by('-created_at')[:4]
        
        # Get categories from actual projects
        categories = Category.objects.filter(
            project_done__service=service,
            project_done__status=True,
            status=True
        ).distinct()
        
        # Fallback to any active categories
        if not categories.exists():
            categories = Category.objects.filter(status=True).distinct()

        # Get service testimonials and FAQs
        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)
        service_faqs = Services_faq.objects.filter(service=service, status='published')

        context = {
            'service': service,
            'related_projects': related_projects,
            'related_projects_logo': related_projects_logo,
            'categories': categories,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
        }
        
        return render(request, 'Frontend/smm.html', context)
    
    except Exception as e:
        print(f"Error in smm view: {str(e)}")
        return render(request, 'Frontend/smm.html', {
            'service': {
                'title': 'Social Media Marketing',
                'sub_title': 'Professional Social Media Marketing Services',
                'description': 'We provide comprehensive social media marketing solutions.'
            },
            'related_projects': Project_done.objects.none(),
            'related_projects_logo': Project_done.objects.none(),
            'categories': Category.objects.none(),
            'service_testimonials': Services_testimonial.objects.none(),
            'service_faqs': Services_faq.objects.none(),
        })
# ===============================================================================
# Digital Marketing Page View
# ===============================================================================
def digital_marketing(request):
    try: 
        # Get service
        service = Services.objects.filter(
            Q(title__icontains='Digital Marketing') | 
            Q(title__icontains='digital') |
            Q(title__icontains='marketing') |
            Q(title__icontains='SEO') |
            Q(title__icontains='Social Media') |
            Q(title__icontains='Content Marketing') |
            Q(title__icontains='Email Marketing') |
            Q(title__icontains='PPC') |
            Q(title__icontains='brand') |
            Q(title__icontains='Online Marketing'),
            status=True
        ).first()
        
        if not service:
            service, _ = Services.objects.get_or_create(
                title='Digital Marketing',
                defaults={
                    'sub_title': 'Professional Digital Marketing Services',
                    'description': 'We provide comprehensive digital marketing solutions including SEO, social media marketing, content marketing, email marketing, and PPC advertising.',
                    'status': True
                }
            )

        # Get additional data
        recent_projects = Project_done.objects.filter(
            service=service, 
            status=True
        ).select_related('service', 'category').order_by('-created_at')[:8]

        if not recent_projects:
            recent_projects = Project_done.objects.filter(
                status=True
            ).select_related('service', 'category').order_by('-created_at')[:8]

        # Get service testimonials
        service_testimonials = Services_testimonial.objects.filter(service=service, status=True)[:3]
        
        # Related projects logo
        related_projects = Project_done.objects.filter(service=service, status=True)
        related_projects_logo = related_projects.exclude(logo='').exclude(logo__isnull=True)

        # Get packages
        packages = Package.objects.filter(status=True)[:3]

        # Get FAQs for this service
        faqs = Services_faq.objects.filter(service=service, status='published')[:5]

        # Initialize forms
        plan_subscriber_form = PlanSubscriberForm()
        custom_package_form = CustomPackageForm()

        # Handle form submissions
        if request.method == 'POST':
            # Check which form was submitted
            if 'package' in request.POST:  # Plan Subscriber form
                plan_subscriber_form = PlanSubscriberForm(request.POST)
                if plan_subscriber_form.is_valid():
                    try:
                        plan_subscriber = plan_subscriber_form.save(commit=False)
                        plan_subscriber.created_at = timezone.now()
                        plan_subscriber.save()

                        # Send thank you email to the requester
                        try:
                            subject = 'Thank you for your package request - BG Infotechs'
                            message = f"""Dear {plan_subscriber.name_business_name},

Thank you for submitting a package request with BG Infotechs. We have received your details and our team will contact you soon.

Your submitted details:
- Name / Business: {plan_subscriber.name_business_name}
- Phone: {plan_subscriber.phone_number}
- Email: {plan_subscriber.email}
- Package: {plan_subscriber.package.title}

If you need to update any information, reply to this email.

Best regards,
BG Infotechs Team
"""
                            send_mail(
                                subject,
                                message,
                                settings.DEFAULT_FROM_EMAIL,
                                [plan_subscriber.email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            print(f"Failed to send customer email for package: {e}")

                        # Notify admin
                        try:
                            admin_subject = f'New Package Request - {plan_subscriber.name_business_name}'
                            admin_message = f"""A new package request has been submitted.

Name / Business: {plan_subscriber.name_business_name}
Phone: {plan_subscriber.phone_number}
Email: {plan_subscriber.email}
Package: {plan_subscriber.package.title}

Submitted at: {plan_subscriber.created_at}

Please follow up with the client.
"""
                            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                            send_mail(
                                admin_subject,
                                admin_message,
                                settings.DEFAULT_FROM_EMAIL,
                                [admin_email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            print(f"Failed to send admin notification for package: {e}")

                        messages.success(request, 'Check your E-mail! Your package request has been submitted successfully! We will contact you soon.')
                        return redirect('frontend_app:digital_marketing')
                        
                    except Exception as e:
                        messages.error(request, f'Error submitting your request: {str(e)}')
                        print(f"Package submission error: {e}")
                else:
                    messages.error(request, 'Please correct the errors in the form.')

            else:  # Custom Package form
                custom_package_form = CustomPackageForm(request.POST)
                if custom_package_form.is_valid():
                    try:
                        custom_package = custom_package_form.save(commit=False)
                        custom_package.created_at = timezone.now()
                        custom_package.save()

                        # Send thank you email to the requester
                        try:
                            subject = 'Thank you for your custom package request - BG Infotechs'
                            message = f"""Dear {custom_package.name_business_name},

Thank you for submitting a custom package request with BG Infotechs. We have received your details and our team will contact you soon.

Your submitted details:
- Name / Business: {custom_package.name_business_name}
- Phone: {custom_package.phone_number}
- Email: {custom_package.email}
- Business Category: {custom_package.business_category}
- Number of Graphics: {custom_package.no_of_graphics}
- Number of Videos: {custom_package.no_of_videos}

If you need to update any information, reply to this email.

Best regards,
BG Infotechs Team
"""
                            send_mail(
                                subject,
                                message,
                                settings.DEFAULT_FROM_EMAIL,
                                [custom_package.email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            print(f"Failed to send customer email for custom package: {e}")

                        # Notify admin
                        try:
                            admin_subject = f'New Custom Package Request - {custom_package.name_business_name}'
                            admin_message = f"""A new custom package request has been submitted.

Name / Business: {custom_package.name_business_name}
Phone: {custom_package.phone_number}
Email: {custom_package.email}
Business Category: {custom_package.business_category}
Number of Graphics: {custom_package.no_of_graphics}
Number of Videos: {custom_package.no_of_videos}
Submitted at: {custom_package.created_at}

Please follow up with the client.
"""
                            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                            send_mail(
                                admin_subject,
                                admin_message,
                                settings.DEFAULT_FROM_EMAIL,
                                [admin_email],
                                fail_silently=True,
                            )
                        except Exception as e:
                            print(f"Failed to send admin notification for custom package: {e}")

                        messages.success(request, 'Check your E-mail! Your custom package request has been submitted successfully! We will contact you soon.')
                        return redirect('frontend_app:digital_marketing')
                        
                    except Exception as e:
                        messages.error(request, f'Error submitting your request: {str(e)}')
                        print(f"Custom package submission error: {e}")
                else:
                    messages.error(request, 'Please correct the errors in the form.')

        context = {
            'service': service,
            'recent_projects': recent_projects,
            'service_testimonials': service_testimonials,
            'packages': packages,
            'related_projects_logo': related_projects_logo,
            'faqs': faqs,
            'plan_subscriber_form': plan_subscriber_form,
            'custom_package_form': custom_package_form,
        }
        return render(request, 'Frontend/digital_marketing.html', context)
    
    except Exception as e:
        print(f"Error in digital_marketing view: {e}")
        # Fallback context if everything fails
        context = {
            'service': {
                'title': 'Digital Marketing', 
                'sub_title': 'Professional Digital Marketing Services',
                'description': 'We provide comprehensive digital marketing solutions including SEO, social media marketing, content marketing, email marketing, and PPC advertising.'
            },
            'recent_projects': [],
            'service_testimonials': [],
            'packages': Package.objects.filter(status=True)[:3],
            'faqs': [],
            'plan_subscriber_form': PlanSubscriberForm(),
            'custom_package_form': CustomPackageForm(),
        }
        return render(request, 'Frontend/digital_marketing.html', context)

def all_digital_marketing(request):
    try:
        dm_keywords = [
            'digital', 'marketing', 'seo', 'SEO', 'social', 'content', 'email', 'ppc',
            'advertising', 'online', 'brand', 'social', 'smm', 'Social Media', 'media marketing', 'social media marketing',
            'facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok',
            'content creation', 'influencer', 'community management', 'social advertising',
        ]
        q_objects = Q()
        for kw in dm_keywords:
            q_objects |= Q(title__icontains=kw)

        service = Services.objects.filter(q_objects, status=True).first()
        if not service:
            service = Services.objects.filter(status=True).first()

        # Base queryset for projects
        if service:
            projects_qs = Project_done.objects.filter(
                service=service,
                status=True
            ).select_related('category', 'service').order_by('-created_at')
        else:
            projects_qs = Project_done.objects.filter(
                status=True
            ).select_related('category', 'service').order_by('-created_at')

        # Search
        search_query = request.GET.get('search', '').strip()
        if search_query:
            projects_qs = projects_qs.filter(
                Q(title__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Category filtering
        category_filter = request.GET.get('category', '').strip()
        active_category = None
        if category_filter:
            try:
                active_category = Category.objects.get(id=category_filter, status=True)
                projects_qs = projects_qs.filter(category=active_category)
            except Category.DoesNotExist:
                active_category = None

        # Categories derived from full queryset (not paginated page)
        categories = Category.objects.filter(
            project_done__in=Project_done.objects.filter(status=True),
            status=True
        ).distinct()
        # Alternatively, restrict categories to those present in projects_qs
        try:
            categories = Category.objects.filter(
                project_done__in=projects_qs,
                status=True
            ).distinct()
        except Exception:
            pass

        # Category counts
        category_counts = {}
        for cat in categories:
            category_counts[cat.id] = Project_done.objects.filter(status=True, category=cat).count()

        # Pagination
        page_size = 6
        paginator = Paginator(projects_qs, page_size)
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Testimonials and FAQs
        if service:
            service_testimonials = Services_testimonial.objects.filter(service=service, status=True)
            service_faqs = Services_faq.objects.filter(service=service, status='published')
        else:
            service_testimonials = Services_testimonial.objects.filter(status=True)
            service_faqs = Services_faq.objects.filter(status='published')

        context = {
            'service': service,
            'projects': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': page_obj.has_other_pages(),
            'search_query': search_query,
            'categories': categories,
            'category_filter': category_filter,
            'active_category': active_category,
            'category_counts': category_counts,
            'service_testimonials': service_testimonials,
            'service_faqs': service_faqs,
        }

        if request.GET.get('ajax'):
            return render(request, 'Frontend/all_digital_marketing_partial.html', context)
        return render(request, 'Frontend/all_digital_marketing.html', context)

    except Exception as e:
        print(f"Error in all_digital_marketing view: {e}")
        return render(request, 'Frontend/all_digital_marketing.html', {
            'service': None,
            'projects': Project_done.objects.none(),
            'page_obj': None,
            'paginator': None,
            'is_paginated': False,
            'search_query': '',
            'categories': Category.objects.none(),
            'category_filter': '',
            'active_category': None,
            'category_counts': {},
            'service_testimonials': Services_testimonial.objects.none(),
            'service_faqs': Services_faq.objects.none(),
        })
    
# Training Page View.....................................................................
def training(request):
    # Start with all active courses
    courses = Course.objects.filter(status=True).order_by('-created_at')
    
    # Get category from request
    category = request.GET.get('category', '').strip().lower()
    
    # Apply category filter if specified
    if category and category != 'all':
        if category == 'web development':
            courses = courses.filter(
                Q(title__icontains='web') | 
                Q(title__icontains='php_with_laravel') |
                Q(title__icontains='java_with_Spring') |
                Q(title__icontains='frontend_development') |
                Q(title__icontains='full_stack') |
                Q(title__icontains='mern_stack') |
                Q(title__icontains='backend_development') |
                Q(title__icontains='python_with_django') |
                Q(title__icontains='development')
            )
        elif category == 'mobile development':
            courses = courses.filter(
                Q(title__icontains='mobile') | 
                Q(title__icontains='mobile_app_development') | 
                Q(title__icontains='app_development') | 
                Q(title__icontains='flutter') | 
                Q(title__icontains='app')
            )
        elif category == 'data science':
            courses = courses.filter(
                Q(title__icontains='data') | 
                Q(title__icontains='data_science') |
                Q(title__icontains='science')  
            )
        elif category == 'cyber security':
            courses = courses.filter(
                Q(title__icontains='cyber') | 
                Q(title__icontains='cyber_security') |
                Q(title__icontains='ethical_hacking') |
                Q(title__icontains='security') |
                Q(title__icontains='hacking')
            )
        elif category == 'ui/ux design':
            courses = courses.filter(
                Q(title__icontains='ui') | 
                Q(title__icontains='ui/ux') |
                Q(title__icontains='ui_ux_design') |
                Q(title__icontains='ux') 
               
            )
        elif category == 'digital marketing':
            courses = courses.filter(
                Q(title__icontains='marketing') |
                Q(title__icontains='digital_marketing') | 
                Q(title__icontains='digital') |
                Q(title__icontains='seo')
            )
        elif category == 'cloud computing':
            courses = courses.filter(
                Q(title__icontains='cloud') | 
                Q(title__icontains='cloud_computing') | 
                Q(title__icontains='aws') |
                Q(title__icontains='computing') 
            )
        elif category == 'networking':
            courses = courses.filter(
                Q(title__icontains='network') | 
                Q(title__icontains='networking') 
            )
        elif category == 'graphic design':
            courses = courses.filter(
                Q(title__icontains='graphic') | 
                Q(title__icontains='graphic_design') 
                
            )
    
    # Search functionality (works with or without category filter)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()
    
    # Get initial 4 courses for display
    initial_courses = courses[:4]
    
    # Compute enrollment counts for ALL courses (for the initial display)
    course_enrollment_qs = CourseEnrollment.objects.values('course').annotate(count=CountFunc('id'))
    course_enrollment_count = {}
    
    try:
        for item in course_enrollment_qs:
            key = item.get('course')
            if key is not None:
                course_enrollment_count[int(key)] = item.get('count', 0)
    except Exception:
        course_enrollment_count = {str(item.get('course')): item.get('count', 0) for item in course_enrollment_qs}
    
    # Add enrollment count to initial courses
    for course in initial_courses:
        try:
            pk_key = int(getattr(course, 'pk', None))
            course.enrolled_students = course_enrollment_count.get(pk_key, 0)
        except Exception:
            course.enrolled_students = course_enrollment_count.get(str(getattr(course, 'pk', None)), 0)
    
    # Get category counts for the filter buttons
    category_counts = {
        'all': Course.objects.filter(status=True).count(),
        'web_development': Course.objects.filter(
            Q(title__icontains='web') | 
            Q(title__icontains='php_with_laravel') |
            Q(title__icontains='java_with_Spring') |
            Q(title__icontains='frontend_development') |
            Q(title__icontains='full_stack') |
            Q(title__icontains='mern_stack') |
            Q(title__icontains='backend_development') |
            Q(title__icontains='python_with_django') |
            Q(title__icontains='development'),
           
            status=True
        ).count(),
        'mobile_development': Course.objects.filter(
            Q(title__icontains='mobile') | 
            Q(title__icontains='mobile_app_development') | 
            Q(title__icontains='app_development') | 
            Q(title__icontains='flutter') | 
            Q(title__icontains='app'),
           
            status=True
        ).count(),
        'data_science': Course.objects.filter(
            Q(title__icontains='data') | 
            Q(title__icontains='data_science') |
            Q(title__icontains='science') ,
            
            status=True
        ).count(),
        'cyber_security': Course.objects.filter(
            Q(title__icontains='cyber') | 
            Q(title__icontains='cyber_security') |
            Q(title__icontains='ethical_hacking') |
            Q(title__icontains='security') |
            Q(title__icontains='hacking'),

            status=True
        ).count(),
        'ui_ux_design': Course.objects.filter(
            Q(title__icontains='ui') | 
            Q(title__icontains='ui_ux_design') |
            Q(title__icontains='ui/ux') |
            Q(title__icontains='ux'),

            status=True
        ).count(),
        'digital_marketing': Course.objects.filter(
            Q(title__icontains='marketing') |
            Q(title__icontains='digital_marketing') | 
            Q(title__icontains='digital') |
            Q(title__icontains='seo'),

            status=True
        ).count(),

        'cloud_computing': Course.objects.filter(
            Q(title__icontains='cloud') | 
            Q(title__icontains='cloud_computing') | 
            Q(title__icontains='aws') |
            Q(title__icontains='computing'),
        
            status=True
        ).count(),
        'networking': Course.objects.filter(
            Q(title__icontains='network') | 
            Q(title__icontains='networking') ,

            status=True
        ).count(),
        'graphic_design': Course.objects.filter(
            Q(title__icontains='graphic') | 
            Q(title__icontains='graphic_design') ,

            status=True
        ).count(),
    }
    
    context = {
        'courses': initial_courses,  # Show only 4 courses initially
        'category_counts': category_counts,
        'current_category': category,
        'search_query': search_query,
        'total_courses': courses.count(),  # Total filtered courses count
        'trainings': [],  # Empty as in your original code
    }
    
    return render(request, 'Frontend/training.html', context)

# Course Enrollment View.....................................................................
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk, status=True)
    media_items = Media.objects.filter(course=course, status=True).order_by('order')
    
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course = course
            enrollment.save()
            # Send confirmation email
            try:
                send_enrollment_confirmation_email(enrollment, course)
            except Exception as e:
                # Log the error but don't show to user
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Enrollment submitted successfully! We have sent a confirmation email.')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseEnrollmentForm()
    
    context = {
        'course': course,
        'media_items': media_items,
        'form': form,
    }
    return render(request, 'Frontend/enrollment.html', context)

def all_courses(request):
    courses_qs = Course.objects.filter(status=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        courses_qs = courses_qs.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()

    page_size = 9
    paginator = Paginator(courses_qs, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Compute enrollment counts for displayed courses
    course_enrollment_qs = CourseEnrollment.objects.values('course').annotate(count=models.Count('id'))
    course_enrollment_count = {}
    try:
        for item in course_enrollment_qs:
            key = item.get('course')
            if key is not None:
                course_enrollment_count[int(key)] = item.get('count', 0)
    except Exception:
        course_enrollment_count = {str(item.get('course')): item.get('count', 0) for item in course_enrollment_qs}

    for course in page_obj.object_list:
        try:
            pk_key = int(getattr(course, 'pk', None))
            course.enrolled_students = course_enrollment_count.get(pk_key, 0)
        except Exception:
            # If int conversion fails, try string key, finally fallback to 0
            course.enrolled_students = course_enrollment_count.get(str(getattr(course, 'pk', None)), 0)

    context = {
        'courses': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'course_enrollment_count': course_enrollment_count,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
        'total_courses_count': paginator.count,  # Add this for display
    }

    if request.GET.get('ajax'):
        return render(request, 'Frontend/course_list_partial.html', context)

    return render(request, 'Frontend/all_courses.html', context)

def process_enrollment(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk, status=True)
        
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
      
        existing_enrollment = CourseEnrollment.objects.filter(
            course=course,
            email=email,
            contact_number=contact_number
        ).first()
        if existing_enrollment:
            messages.info(request, 'You have already enrolled in this course! We will contact you soon.')
            return redirect('frontend_app:training')
        # Create enrollment from form data
        enrollment = CourseEnrollment(
            course=course,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=email,
            contact_number=contact_number,
            address=request.POST.get('address'),
            education=request.POST.get('education'),
            experience=request.POST.get('experience'),
            source=request.POST.get('source'),
        )
        try:
            enrollment.save()
            # Send confirmation email
            try:
                send_enrollment_confirmation_email(enrollment, course)
            except Exception as e:
                print(f"Email sending failed: {e}")
            messages.success(request, 'Enrollment submitted successfully! Check your email for confirmation.')
            return redirect('frontend_app:training')
        except Exception as e:
            messages.error(request, f'Error submitting enrollment: {str(e)}')
            return redirect('frontend_app:enroll_course', pk=pk)
    
    return redirect('frontend_app:enroll_course', pk=pk)

def course_detail(request, pk):
    # Get the main course object
    main_course = get_object_or_404(Course, pk=pk, status=True)
    media_items = Media.objects.filter(course=main_course, status=True).order_by('order')
    
    # Get all courses for the sidebar/course list
    courses_qs = Course.objects.filter(status=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        courses_qs = courses_qs.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()

    # Pagination
    page_size = 9
    paginator = Paginator(courses_qs, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Compute enrollment counts for displayed courses in the paginated list
    course_enrollment_qs = CourseEnrollment.objects.values('course').annotate(count=models.Count('id'))
    course_enrollment_count = {}
    
    try:
        for item in course_enrollment_qs:
            key = item.get('course')
            if key is not None:
                course_enrollment_count[int(key)] = item.get('count', 0)
    except Exception:
        course_enrollment_count = {str(item.get('course')): item.get('count', 0) for item in course_enrollment_qs}

    # Add enrollment count to each course in the paginated list
    for course_item in page_obj.object_list:
        try:
            pk_key = int(getattr(course_item, 'pk', None))
            course_item.enrolled_students = course_enrollment_count.get(pk_key, 0)
        except Exception:
            course_item.enrolled_students = course_enrollment_count.get(str(getattr(course_item, 'pk', None)), 0)

    # Get enrollment count for the main course
    main_course_enrollment_count = course_enrollment_count.get(main_course.pk, 0)
    
    context = {
        'course': main_course,  # The main course being viewed
        'media_items': media_items,
        'page_obj': page_obj,  # Paginated courses for sidebar
        'enrolled_students': main_course_enrollment_count,  # Enrollment count for main course
    }
    return render(request, 'Frontend/course_detail.html', context)


# Email sending function
def send_enrollment_confirmation_email(enrollment, course):
    """Send enrollment confirmation email to student"""
    subject = f'Course Enrollment Confirmation - {course.title}'
    
    message = f"""
Dear {enrollment.first_name} {enrollment.last_name},

Thank you for enrolling in our "{course.title}" course at BG Infotechs!

**Enrollment Details:**
- Course: {course.title}
- Duration: {course.duration_display()}
- Enrollment Date: {enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M')}
- Enrollment ID: {enrollment.id}

**What's Next?**
1. Our team will contact you within 24 hours to confirm your enrollment
2. You will receive course materials and schedule details
3. Get ready to start your learning journey!

**Course Overview:**
{course.short_description}

**Contact Information:**
If you have any questions, please contact us at:
- Phone: +977-9842251119
- Email: info@bginfotechs.com
- Address: BG Infotechs, Dhangadhi, Nepal

We're excited to have you in our course and look forward to helping you achieve your learning goals!

Best regards,
BG Infotechs Team
www.bginfotechs.com
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [enrollment.email],
        fail_silently=True,
    )
    # Notify admin about new enrollment
    admin_subject = f'New Course Enrollment - {course.title}'
    admin_message = f"""
New course enrollment received:

**Student Information:**
- Name: {enrollment.first_name} {enrollment.last_name}
- Email: {enrollment.email}
- Phone: {enrollment.contact_number}
- Education: {enrollment.get_education_display()}
- Experience: {enrollment.get_experience_display()}
- Source: {enrollment.get_source_display()}

**Course Details:**
- Course: {course.title}
- Enrollment ID: {enrollment.id}
- Enrollment Date: {enrollment.enrolled_at}

Please follow up with the student within 24 hours.
"""
    
    # Send to admin email (you can set this in settings or use a default)
    admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
    send_mail(
        admin_subject,
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        [admin_email],
        fail_silently=True,
    )

# Features Page View.....................................................................
def features(request):
    all_features = Features.objects.filter(status=True)
    
    context = {
        'features': all_features,
    }
    return render(request, 'Frontend/features.html', context)

# Blog List View ..........................................................................
def blogs(request):
    # Get published blogs without using category field
    blogs_list = Blog.objects.filter(status='published').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        blogs_list = blogs_list.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Limit results
    blogs_list = blogs_list[:6]
    
    context = {
        'blogs': blogs_list,
        'search_query': search_query,
    }
    return render(request, 'Frontend/Blog.html', context)  

def blog_list(request):
    # Get published blogs queryset with select_related for performance
    blogs_qs = Blog.objects.filter(status='published').select_related(
        'category', 'author'
    ).order_by('-published_at', '-created_at')

    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        blogs_qs = blogs_qs.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()

    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        blogs_qs = blogs_qs.filter(category__name__icontains=category_filter)

    page_size = 12
    paginator = Paginator(blogs_qs, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    from blog_app.models import Category  
    published_category_ids = Blog.objects.filter(
        status='published'
    ).exclude(category__isnull=True).values_list('category_id', flat=True).distinct()
    
    categories = Category.objects.filter(
        id__in=published_category_ids
    ).order_by('name')

    context = {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
        'categories': categories,
        'category_filter': category_filter,
    }
    
    if request.GET.get('ajax'):
        return render(request, 'Frontend/blog_list_partial.html', context)
    
    return render(request, 'Frontend/blog_list.html', context)

def blog_details(request, slug):
    """Public blog detail view - no authentication required"""
    
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    comments = blog.comments.filter(status=BlogComment.Status.APPROVED).order_by('-created_at')
    
    popular_posts = Blog.objects.filter(
        status='published'
    ).exclude(
        id=blog.id
    ).order_by('-published_at', '-created_at')[:5]
    
    from django.db.models import Count, Q
    from blog_app.models import Category  
    from django.db.models import Count
    
    categories = Category.objects.all().order_by('name')
    published_category_ids = Blog.objects.filter(
        status='published'
    ).exclude(category__isnull=True).values_list('category_id', flat=True).distinct()
    
    categories_with_blogs = Category.objects.filter(
        id__in=published_category_ids
    ).order_by('name')

    category_counts_qs = Blog.objects.filter(
        status='published',
        category__isnull=False
    ).values('category').annotate(total=Count('id'))

    category_blog_count = {item['category']: item['total'] for item in category_counts_qs}

    try:
        categories_with_blogs = Category.objects.filter(
            id__in=[item['category'] for item in category_counts_qs]
        ).annotate(blog_count=Count('blog')).order_by('name')
    except Exception:
      
        categories_with_blogs = Category.objects.filter(
            id__in=published_category_ids
        ).order_by('name')
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validation
        if len(comment_text) < 10:
            messages.error(request, 'Comment must be at least 10 characters long.')
        elif len(comment_text) > 1000:
            messages.error(request, 'Comment cannot exceed 1000 characters.')
        elif not full_name:
            messages.error(request, 'Please provide your full name.')
        elif not email:
            messages.error(request, 'Please provide your email address.')
        else:
            BlogComment.objects.create(
                blog=blog,
                comment=comment_text,
                full_name=full_name,
                email=email,
                status=BlogComment.Status.PENDING  
            )
            messages.success(request, 'Your comment has been submitted and is awaiting approval!')
            return redirect('frontend_app:blog_details', slug=blog.slug)
    
    context = {
        'blog': blog,
        'comments': comments,
        'popular_posts': popular_posts,
        'categories': categories_with_blogs,  
        'category_blog_count': category_blog_count,
        'page_title': blog.title,
    }
    return render(request, 'Frontend/blog_details.html', context)

def blog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blogs_list = Blog.objects.filter(
        status='published', 
        category=category
    ).order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'blogs': blogs_list,
        'categories': categories,
        'selected_category': category_slug,
        'category_name': category.name,
    }
    return render(request, 'Frontend/blog_category.html', context)

# Career Page View..........................................................................
def careers(request):
    try:
        vacancies = Vacancy.objects.filter(status='active').order_by('-created_at')[:6]
    except Exception:
        vacancies = Vacancy.objects.filter(status='active').order_by('-id')[:6]
    
    # Add expiry status calculation (same as all_careers view)
    today = timezone.now().date()
    for vacancy in vacancies:
        days_remaining = (vacancy.expired_date - today).days
        
        if days_remaining < 0:
            vacancy.expiry_status = "expired"
            vacancy.expiry_text = "Expired"
        elif days_remaining == 0:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = "Expires today"
        elif days_remaining == 1:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = "Expires tomorrow"
        elif days_remaining <= 7:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = f"Expires in {days_remaining} days"
        else:
            vacancy.expiry_status = "active"
            vacancy.expiry_text = f"Expires in {days_remaining} days"
    
    context = {
        'vacancies': vacancies,
        'today': today,  # Also include today in context for consistency
    }
    return render(request, 'Frontend/career.html', context)

def all_careers(request):
    search_query = request.GET.get('search', '').strip()
    vacancies_qs = Vacancy.objects.filter(status='active')

    # Apply search across several likely fields
    if search_query:
        search_filters = (
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(job_type__icontains=search_query) 
        )
        vacancies_qs = vacancies_qs.filter(search_filters)

    vacancies_list = vacancies_qs.order_by('-created_at')
    paginator = Paginator(vacancies_list, 10)  # 10 vacancies per page
    page_number = request.GET.get('page', 1)

    try:
        vacancies = paginator.page(page_number)
    except PageNotAnInteger:
        vacancies = paginator.page(1)
    except EmptyPage:
        vacancies = paginator.page(paginator.num_pages)

    today = timezone.now().date()
    for vacancy in vacancies:
        days_remaining = (vacancy.expired_date - today).days
        
        if days_remaining < 0:
            vacancy.expiry_status = "expired"
            vacancy.expiry_text = "Expired"
        elif days_remaining == 0:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = "Expires today"
        elif days_remaining == 1:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = "Expires tomorrow"
        elif days_remaining <= 7:
            vacancy.expiry_status = "closing_soon"
            vacancy.expiry_text = f"Expires in {days_remaining} days"
        else:
            vacancy.expiry_status = "active"
            vacancy.expiry_text = f"Expires in {days_remaining} days"

    context = {
        'vacancies': vacancies,
        'search_query': search_query,
        'today': today,
    }
    return render(request, 'Frontend/all_careers.html', context)

def career_details(request, pk):
    vacancy = get_object_or_404(Vacancy, status='active', pk=pk)
    
    has_applied = False
    applicant_email = ""
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            
            # Check for duplicate application by email
            applicant_email = application.email
            if JobApplication.objects.filter(vacancy=vacancy, email=applicant_email).exists():
                messages.warning(request, 'You have already applied for this position with this email address.')
                has_applied = True
            else:
                application.save()
                messages.success(request, 'Your application has been submitted successfully! We will contact you soon.')
                
                # Send confirmation email (optional)
                try:
                    send_mail(
                        f'Application Received - {vacancy.title}',
                        f'Dear {application.full_name},\n\nThank you for applying to the {vacancy.title} position at BG-Infotechs. We have received your application and will review it carefully.\n\nBest regards,\nBG-Infotechs Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [application.email],
                        fail_silently=True,
                    )
                except:
                    pass  
                
                return redirect('frontend_app:career_details', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobApplicationForm()
    
    if not has_applied and request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            has_applied = JobApplication.objects.filter(vacancy=vacancy, email=email).exists()
    
    context = {
        'vacancy': vacancy,
        'form': form,
        'has_applied': has_applied,
        'is_active': vacancy.is_active(),
    }
    return render(request, 'Frontend/career_details.html', context)

def my_applications(request):
    """
    View to check application status by email
    """
    applications = []
    email = ""
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            applications = JobApplication.objects.filter(email=email).select_related('vacancy').order_by('-applied_at')
            if not applications:
                messages.info(request, 'No applications found for this email address.')
        else:
            messages.error(request, 'Please enter your email address.')
    
    context = {
        'applications': applications,
        'email': email,
    }
    return render(request, 'Frontend/my_applications.html', context)

# Contact Page View................................................................
def contact(request):
    # Get all active branches from database
    branches = Branch.objects.filter(status=True)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create contact but don't save yet
            contact = form.save(commit=False)
            # Set additional fields
            contact.status = True  # Set as active
            contact.is_read = False  # Set as unread
            contact.save()
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            # Use the correct URL name based on where your view is located
            return redirect('frontend_app:contact')  # or 'contact_app:contact' depending on your setup
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'branches': branches,
        'form': form,
    }
    return render(request, 'Frontend/contact.html', context)


def terms_conditions(request):
    return render(request, 'Frontend/terms_conditions.html')

def privacy_policy(request):
    return render(request, 'Frontend/privacy_policy.html')

# Error Handlers........................................................................
def handler404(request, exception):
    """Handle 404 errors with custom template"""
    print(f"404 Error: {exception}")  # For debugging
    return render(request, 'Frontend/404.html', status=404)

def handler500(request):
    """Handle 500 errors with custom template"""
    return render(request, 'Frontend/500.html', status=500)

def handler403(request, exception):
    """Handle 403 errors with custom template"""
    return render(request, 'Frontend/403.html', status=403)

def handler400(request, exception):
    """Handle 400 errors with custom template"""
    return render(request, 'Frontend/400.html', status=400)

def handler404_override(request, undefined_path):
    """Custom handler for undefined URLs that redirects to the 404 page"""
    return handler404(request, None)