from django.contrib import admin
from .models import Vacancy, JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'vacancy', 'email', 'status', 'applied_at']
    list_filter = ['status', 'applied_at', 'vacancy']
    search_fields = ['full_name', 'email', 'vacancy__title']
    readonly_fields = ['applied_at', 'updated_at']

admin.site.register(Vacancy)