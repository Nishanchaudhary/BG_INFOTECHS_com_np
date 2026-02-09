from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Package, PlanSubscriber, CustomPackage

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'month_price', 'year_price', 'status')
    search_fields = ('title', 'tags')
    list_filter = ('status',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height:60px;"/>')
        return ""
    image_preview.short_description = 'Image Preview'

@admin.register(PlanSubscriber)
class PlanSubscriberAdmin(admin.ModelAdmin):
    list_display = ('name_business_name', 'email', 'phone_number', 'package')
    search_fields = ('name_business_name', 'email', 'phone_number')
    list_filter = ('package',)

@admin.register(CustomPackage)
class CustomPackageAdmin(admin.ModelAdmin):
    list_display = ('name_business_name', 'email', 'phone_number', 'business_category')
    search_fields = ('name_business_name', 'email', 'business_category')
