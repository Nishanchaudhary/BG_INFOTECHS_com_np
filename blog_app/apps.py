from django.apps import AppConfig

class BlogsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_app'  
    verbose_name = 'Blog Application'