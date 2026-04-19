from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from locations.models import District
from providers.models import ProviderProfile
from categories.models import MainCategory, SubCategory


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import UserProfile
from providers.models import ProviderProfile
from locations.models import District
from categories.models import MainCategory, SubCategory


def auth_page(request):

    districts = District.objects.all()
    main_categories = MainCategory.objects.filter(is_active=True)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ================= LOGIN =================
        if form_type == "login":

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                # ✅ SUPER ADMIN
                if user.is_superuser:
                    return redirect("admin_dashboard")

                profile = UserProfile.objects.filter(user=user).first()

                if not profile:
                    messages.error(request, "Account setup incomplete.")
                    logout(request)
                    return redirect("auth_page")

                # ✅ PROVIDER LOGIN
                if profile.role == "provider":

                    provider = ProviderProfile.objects.filter(user=user).first()

                    if not provider:
                        logout(request)
                        return redirect("auth_page")

                    # approval check
                    if provider.status in ["pending", "rejected"]:
                        return redirect("provider_waiting")

                    # profile completion check
                    if not provider.business_description or not provider.logo:
                        return redirect("provider_complete_profile")

                    return redirect("provider_dashboard")

                # ✅ NORMAL USER
                return redirect("user_dashboard")

            else:
                messages.error(request, "Invalid username or password")
                return redirect("auth_page")

        # ================= USER SIGNUP =================
        elif form_type == "user_signup":

            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("auth_page")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # ✅ ROLE = USER
            UserProfile.objects.create(user=user, role="user")

            messages.success(request, "Account created successfully! Please login.")
            return redirect("auth_page")

        # ================= PROVIDER SIGNUP =================
        elif form_type == "provider_signup":

            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            business_name = request.POST.get("business_name")
            phone = request.POST.get("phone")
            subcategory_id = request.POST.get("subcategory")
            district_id = request.POST.get("district")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("auth_page")

            # create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # ✅ SAFE PROFILE CREATION
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = "provider"
            profile.save()

            # related objects
            district = District.objects.get(id=district_id)
            subcategory = SubCategory.objects.get(id=subcategory_id)

            # create provider profile
            ProviderProfile.objects.create(
                user=user,
                business_name=business_name,
                phone=phone,
                district=district,
                subcategory=subcategory,
                full_address="Temporary address",
                status="pending"
            )

            messages.success(request, "Provider registered! Wait for admin approval.")
            return redirect("auth_page")

    return render(request, "accounts/auth.html", {
        "districts": districts,
        "main_categories": main_categories
    })

def logout_view(request):
    logout(request)
    return redirect("auth_page")


# ================= PROVIDER WAITING PAGE =================

@login_required
def provider_waiting(request):

    try:
        provider = ProviderProfile.objects.get(user=request.user)
    except ProviderProfile.DoesNotExist:
        return redirect("auth_page")

    return render(request, "accounts/provider_waiting.html", {
        "status": provider.status
    })


# ================= AJAX SUBCATEGORY FETCH =================

def get_subcategories(request):

    main_category_id = request.GET.get("main_category_id")

    subcategories = SubCategory.objects.filter(
        main_category_id=main_category_id,
        is_active=True
    ).values("id", "name")

    return JsonResponse(list(subcategories), safe=False)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from locations.models import District


@login_required
def user_profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    districts = District.objects.all()

    if request.method == "POST":

        # Update User model
        request.user.username = request.POST.get("name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update Profile
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        district_id = request.POST.get("district")
        if district_id:
            profile.district_id = district_id

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        profile.save()

        return redirect("user_profile")

    return render(request, "users/profile.html", {
        "profile": profile,
        "districts": districts
    })