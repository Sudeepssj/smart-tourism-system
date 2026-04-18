from django.contrib import admin
from .models import Service, ServiceGallery


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "subcategory", "booking_type", "price")
    list_filter = ("booking_type", "subcategory")


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceGallery)