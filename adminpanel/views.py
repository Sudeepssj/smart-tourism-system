from django.shortcuts import render ,  redirect
from django.contrib.auth.models import User
from accounts.models import UserProfile
from providers.models import ProviderProfile
from locations.models import District
from .decorators import admin_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from categories.models import MainCategory, SubCategory




from providers.models import ProviderProfile
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@admin_required
def admin_dashboard(request):

    total_users = User.objects.count()
    total_districts = District.objects.count()
    total_providers = ProviderProfile.objects.count()
    pending_count = ProviderProfile.objects.filter(status="pending").count()

    context = {
        "total_users": total_users,
        "total_districts": total_districts,
        "total_providers": total_providers,
        "pending_count": pending_count,
    }

    return render(request, "adminpanel/dashboard.html", context)


from django.contrib import messages
from locations.models import District
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import admin_required


@login_required
@admin_required
def add_district(request):

    if request.method == "POST":
        name = request.POST.get("name")
        state = request.POST.get("state")

        if not name or not state:
            messages.error(request, "All fields are required.")
            return redirect("add_district")

        # Prevent duplicate district in same state
        if District.objects.filter(name__iexact=name, state__iexact=state).exists():
            messages.warning(request, "District already exists in this state.")
            return redirect("add_district")

        District.objects.create(name=name, state=state)

        messages.success(request, "District added successfully ✅")
        return redirect("add_district")

    return render(request, "adminpanel/districts/add_district.html")

# Manage Page View
@login_required
@admin_required
def district_list(request):
    districts = District.objects.all().order_by("-id")
    return render(request, "adminpanel/districts/manage_districts.html", {
        "districts": districts
    })


# AJAX Update District
@require_POST
@login_required
@admin_required
def update_district(request):
    district_id = request.POST.get("id")
    name = request.POST.get("name")
    state = request.POST.get("state")

    district = District.objects.get(id=district_id)
    district.name = name
    district.state = state
    district.save()

    return JsonResponse({"status": "success"})

# AJAX Delete District
@require_POST
@login_required
@admin_required
def delete_district(request):
    district_id = request.POST.get("id")
    District.objects.get(id=district_id).delete()

    total = District.objects.count()

    return JsonResponse({
        "status": "success",
        "total_districts": total
    })



    

from django.contrib.auth.decorators import login_required
from adminpanel.decorators import admin_required

@login_required
@admin_required
def pending_providers(request):

    providers = ProviderProfile.objects.filter(status="pending")

    return render(request,
                  "adminpanel/providers/pending_providers.html",
                  {"providers": providers})


@login_required
@admin_required
def approved_providers(request):

    providers = ProviderProfile.objects.filter(status="approved")

    return render(request,
                  "adminpanel/providers/approved_providers.html",
                  {"providers": providers})


@require_POST
@login_required
@admin_required
def update_provider_status(request):

    provider_id = request.POST.get("provider_id")
    action = request.POST.get("action")

    provider = ProviderProfile.objects.get(id=provider_id)

    if action == "approve":
        provider.status = "approved"
    elif action == "reject":
        provider.status = "rejected"

    provider.save()

    return JsonResponse({"success": True})


@login_required
@admin_required
def rejected_providers(request):

    providers = ProviderProfile.objects.filter(status="rejected")

    search = request.GET.get("search")

    if search:
        providers = providers.filter(name__icontains=search)

    return render(request,
                  "adminpanel/providers/rejected_providers.html",
                  {"providers": providers})

def admin_main_categories(request):

    categories = MainCategory.objects.all()

    return render(request, "adminpanel/main_categories.html", {
        "categories": categories
    })


def admin_add_main_category(request):

    if request.method == "POST":

        name = request.POST.get("name")

        MainCategory.objects.create(name=name)

        return redirect("admin_main_categories")

    return render(request, "adminpanel/add_main_category.html")

def admin_sub_categories(request):

    subcategories = SubCategory.objects.select_related("main_category")

    return render(request, "adminpanel/sub_categories.html", {
        "subcategories": subcategories
    })


def admin_add_sub_category(request):

    categories = MainCategory.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        SubCategory.objects.create(
            name=name,
            main_category_id=category_id,
            image=image
        )

        return redirect("admin_sub_categories")

    return render(request, "adminpanel/add_sub_category.html", {
        "categories": categories
    })

from categories.models import MainCategory, SubCategory
from django.shortcuts import get_object_or_404

def edit_main_category(request, id):

    category = get_object_or_404(MainCategory, id=id)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("admin_main_categories")

    return render(request, "adminpanel/edit_main_category.html", {
        "category": category
    })


def delete_main_category(request, id):

    category = get_object_or_404(MainCategory, id=id)

    # Prevent delete if subcategories exist
    if category.subcategories.exists():
        messages.error(request, "Are you sure you want to delete this category? Subcategories must be deleted first.")
        return redirect("admin_main_categories")

    category.delete()

    messages.success(request, "Main Category deleted successfully.")
    return redirect("admin_main_categories")


def edit_sub_category(request, id):

    subcategory = get_object_or_404(SubCategory, id=id)
    categories = MainCategory.objects.all()

    if request.method == "POST":

        subcategory.name = request.POST.get("name")
        subcategory.main_category_id = request.POST.get("category")

        image = request.FILES.get("image")

        # update image only if new one uploaded
        if image:
            subcategory.image = image

        subcategory.save()

        return redirect("admin_sub_categories")

    return render(request, "adminpanel/edit_sub_category.html", {
        "subcategory": subcategory,
        "categories": categories
    })

def delete_sub_category(request, id):

    subcategory = get_object_or_404(SubCategory, id=id)

    subcategory.delete()

    messages.success(request, "Sub Category deleted successfully.")
    return redirect("admin_sub_categories")



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserProfile
from providers.models import ProviderProfile


@login_required
def admin_users(request):

    users = User.objects.all().select_related()

    data = []

    total_users = 0
    total_providers = 0

    for user in users:

        profile = UserProfile.objects.filter(user=user).first()

        role = profile.role if profile else "user"

        if role == "provider":
            total_providers += 1
        else:
            total_users += 1

        provider = ProviderProfile.objects.filter(user=user).first()

        main_category = "-"
        subcategory = "-"

        if provider:
            if provider.subcategory:
                subcategory = provider.subcategory.name
                main_category = provider.subcategory.main_category.name

        data.append({
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "role": role,
            "main_category": main_category,
            "subcategory": subcategory,
            "is_active": user.is_active,
        })
                

    context = {
        "data": data,
        "total_users": total_users,
        "total_providers": total_providers,
    }

    return render(request, "adminpanel/users.html", context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def toggle_user_status(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # Prevent admin disabling themselves
    if user == request.user:
        messages.error(request, "You cannot disable your own account.")
        return redirect("admin_users")

    # Toggle status
    if user.is_active:
        user.is_active = False
        messages.success(request, f"{user.username} has been disabled.")
    else:
        user.is_active = True
        messages.success(request, f"{user.username} has been enabled.")

    user.save()

    return redirect("admin_users")


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Avg
from reviews.models import Review
from categories.models import MainCategory, SubCategory
from providers.models import ProviderProfile


def admin_reviews(request):

    reviews = Review.objects.select_related(
        "user", "service", "service__provider", "service__subcategory"
    ).order_by("-created_at")

    # 🔽 FILTER VALUES FROM URL
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    provider_id = request.GET.get("provider")
    search = request.GET.get("search")

    # 🔍 APPLY FILTERS

    if category_id:
        reviews = reviews.filter(
            service__subcategory__main_category_id=category_id
        )

    if subcategory_id:
        reviews = reviews.filter(
            service__subcategory_id=subcategory_id
        )

    if provider_id:
        reviews = reviews.filter(
            service__provider_id=provider_id
        )

    if search:
        reviews = reviews.filter(
            user__username__icontains=search
        ) | reviews.filter(
            service__title__icontains=search
        )

    # 📊 STATS
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    # 📄 PAGINATION
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # 🔽 DROPDOWN DATA
    categories = MainCategory.objects.all()
    subcategories = SubCategory.objects.all()
    providers = ProviderProfile.objects.all()

    context = {
        "page_obj": page_obj,
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "categories": categories,
        "subcategories": subcategories,
        "providers": providers,
        "selected_category": category_id,
        "selected_subcategory": subcategory_id,
        "selected_provider": provider_id,
        "search": search,
    }

    return render(request, "adminpanel/reviews.html", context)

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from reviews.models import Review

def delete_review_admin(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    review.delete()

    messages.success(request, "Review deleted successfully")

    return redirect("admin_reviews")