from django.urls import path
from . import views

urlpatterns = [

    path("create/<int:service_id>/",views.create_booking,name="create_booking"),
    path("details/<str:booking_id>/", views.booking_details, name="booking_details"),



]