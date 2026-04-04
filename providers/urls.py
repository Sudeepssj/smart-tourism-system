from django.urls import path
from . import views
from .views import provider_complete_profile, provider_edit_business, provider_my_business


urlpatterns = [
    path("dashboard/", views.provider_dashboard, name="provider_dashboard"),
    path("complete-profile/", provider_complete_profile, name="provider_complete_profile"),
    path("my-business/", provider_my_business, name="provider_my_business"),
    path("my-business/edit/", provider_edit_business, name="provider_edit_business"),
    path("services/", views.service_list, name="service_list"),
    path("services/add/", views.service_add, name="service_add"),
    path("services/edit/<int:pk>/", views.service_edit, name="service_edit"),
    path("services/gallery/<int:pk>/", views.service_gallery, name="service_gallery"),
    path("services/delete/<int:pk>/", views.service_delete, name="service_delete"),
    path("services/image/delete/<int:pk>/", views.service_image_delete, name="service_image_delete"),
    path("bookings/",views.provider_bookings,name="provider_bookings"),
    path("bookings/update/<str:booking_id>/<str:status>/",views.booking_status_update,name="booking_status_update"),



]



