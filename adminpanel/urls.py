from django.urls import path
from . import views 

urlpatterns = [
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("districts/add/", views.add_district, name="add_district"),
    path("districts/manage/", views.district_list, name="district_list"),
    path("districts/update/", views.update_district, name="update_district"),
    path("districts/delete/", views.delete_district, name="delete_district"),
    path("providers/pending/", views.pending_providers, name="pending_providers"),
    # path("providers/approve/<int:id>/", views.approve_provider, name="approve_provider"),
    # path("providers/reject/<int:id>/", views.reject_provider, name="reject_provider"),
    path("providers/pending/", views.pending_providers, name="pending_providers"),
    path("providers/approved/", views.approved_providers, name="approved_providers"),
    path("providers/status-update/", views.update_provider_status, name="update_provider_status"),
    path("providers/rejected/", views.rejected_providers, name="rejected_providers"),
    path("categories/main/", views.admin_main_categories, name="admin_main_categories"),
    path("categories/sub/", views.admin_sub_categories, name="admin_sub_categories"),
    path("categories/main/add/", views.admin_add_main_category, name="admin_add_main_category"),
    path("categories/sub/add/", views.admin_add_sub_category, name="admin_add_sub_category"),
    # MAIN CATEGORY
    path("categories/main/edit/<int:id>/", views.edit_main_category, name="edit_main_category"),
    path("categories/main/delete/<int:id>/", views.delete_main_category, name="delete_main_category"),

    # SUB CATEGORY
    path("categories/sub/edit/<int:id>/", views.edit_sub_category, name="edit_sub_category"),
    path("categories/sub/delete/<int:id>/", views.delete_sub_category, name="delete_sub_category"),
    
    path("users/", views.admin_users, name="admin_users"),
    path("users/toggle/<int:user_id>/", views.toggle_user_status, name="toggle_user_status"),
    path("reviews/", views.admin_reviews, name="admin_reviews"),
    path("reviews/delete/<int:review_id>/", views.delete_review_admin, name="delete_review_admin"),

]
