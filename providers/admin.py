from django.contrib import admin
from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'business_name',
        'user',
        'phone',
        'district',
        'subcategory',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'district',
        'subcategory'
    )

    search_fields = (
        'business_name',
        'user__username',
        'phone'
    )