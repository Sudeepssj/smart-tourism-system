from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("explore/<int:category_id>/", views.explore_category, name="explore_category"),
    path("services/<int:subcategory_id>/", views.services_by_subcategory, name="services_by_subcategory"),
    path("service/<int:service_id>/",views.service_details,name="service_details"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("cancel-booking/<str:booking_id>/", views.cancel_booking, name="cancel_booking"),


]
