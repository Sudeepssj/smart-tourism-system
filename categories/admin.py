from django.contrib import admin
from .models import MainCategory, SubCategory


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('main_category', 'is_active')