from django.contrib import admin
from .models import Category, Blog, BlogComment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'author', 
        'category', 
        'status', 
        'published_at', 
        'created_at'
    ]
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'short_description', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'published_at']

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = [ 'blog', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['blog__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']