from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.auth_page, name="auth_page"),
    path("logout/", views.logout_view, name="logout"),
    path("provider-status/", views.provider_waiting, name="provider_waiting"),
    path("get-subcategories/", views.get_subcategories, name="get_subcategories"),
]
