from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from providers.models import ProviderProfile
from services.models import Service, ServiceGallery
from django.contrib import messages





@login_required
def provider_dashboard(request):

    # Get provider profile safely
    provider_profile = ProviderProfile.objects.get(user=request.user)

    # IMPORTANT: Filter using ProviderProfile (NOT request.user)
    total_services = Service.objects.filter(provider=provider_profile).count()

    # Reviews will be added later
    total_reviews = 0

    context = {
        "provider": provider_profile,
        "total_services": total_services,
        "total_reviews": total_reviews
    }

    return render(request, "providers/dashboard.html", context)



@login_required
def provider_complete_profile(request):
    provider = ProviderProfile.objects.get(user=request.user)

    if request.method == "POST":
        provider.business_description = request.POST.get("business_description")
        provider.full_address = request.POST.get("full_address")
        provider.website = request.POST.get("website")
        provider.google_map_link = request.POST.get("google_map_link")

        if request.FILES.get("logo"):
            provider.logo = request.FILES.get("logo")

        provider.save()
        return redirect("provider_dashboard")

    return render(request, "providers/complete_profile.html", {
        "provider": provider
    })




@login_required
def provider_my_business(request):
    try:
        provider = ProviderProfile.objects.select_related(
            "subcategory__main_category"
        ).get(user=request.user)
    except ProviderProfile.DoesNotExist:
        return redirect("provider_dashboard")

    context = {
        "provider": provider
    }

    return render(request, "providers/my_business.html", context)

@login_required
def provider_edit_business(request):
    provider = ProviderProfile.objects.get(user=request.user)

    if request.method == "POST":
        provider.business_name = request.POST.get("business_name")
        provider.business_description = request.POST.get("business_description")
        provider.full_address = request.POST.get("full_address")
        provider.phone = request.POST.get("phone")
        provider.alternate_phone = request.POST.get("alternate_phone")
        provider.business_email = request.POST.get("business_email")
        provider.website = request.POST.get("website")
        provider.google_map_link = request.POST.get("google_map_link")
        provider.opening_time = request.POST.get("opening_time")
        provider.closing_time = request.POST.get("closing_time")

        if request.FILES.get("logo"):
            provider.logo = request.FILES.get("logo")

        if request.FILES.get("cover_image"):
            provider.cover_image = request.FILES.get("cover_image")

        provider.save()
        return redirect("provider_my_business")

    return render(request, "providers/edit_business.html", {
        "provider": provider
    })


from services.models import Service
from django.contrib.auth.decorators import login_required

@login_required
def service_list(request):
    provider = ProviderProfile.objects.get(user=request.user)
    services = Service.objects.filter(provider=provider)

    return render(request, "providers/services/service_list.html", {
        "services": services
    })


from services.models import Service, ServiceGallery
from django.shortcuts import render, redirect
from django.contrib import messages

from categories.models import SubCategory
from services.models import Service, ServiceGallery



@login_required
def service_add(request):

    provider = ProviderProfile.objects.get(user=request.user)

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        service = Service.objects.create(
            provider=provider,
            subcategory=provider.subcategory,   # auto assign
            title=title,
            description=description,
            price=price,
            is_available=True
        )

        images = request.FILES.getlist("images")

        for img in images:
            ServiceGallery.objects.create(
                service=service,
                image=img
            )

        messages.success(request, "Service added successfully.")
        return redirect("service_list")

    return render(
        request,
        "providers/services/service_add.html"
    )

@login_required
def service_edit(request, pk):

    provider = ProviderProfile.objects.get(user=request.user)
    service = Service.objects.get(id=pk, provider=provider)

    if request.method == "POST":
        service.title = request.POST.get("title")
        service.description = request.POST.get("description")
        service.price = request.POST.get("price")
        service.offer_price = request.POST.get("offer_price") or None
        service.is_available = request.POST.get("is_available") == "on"
        service.save()
        # Handle additional images
        images = request.FILES.getlist("images")
        for img in images:
            ServiceGallery.objects.create(
                service=service,
                image=img
            )

        messages.success(request, "Service updated successfully.")
        return redirect("service_list")

    return render(request, "providers/services/service_edit.html", {
        "service": service
    })


@login_required
def service_delete(request, pk):

    provider = ProviderProfile.objects.get(user=request.user)
    service = Service.objects.get(id=pk, provider=provider)

    service.delete()

    messages.success(request, "Service deleted successfully.")
    return redirect("service_list")

@login_required
def service_image_delete(request, pk):

    provider = ProviderProfile.objects.get(user=request.user)

    image = ServiceGallery.objects.get(id=pk)

    # Security check
    if image.service.provider != provider:
        return redirect("service_list")

    service_id = image.service.id  # store before delete

    image.delete()

    messages.success(request, "Image deleted successfully.")

    return redirect("service_gallery", pk=service_id)

@login_required
def service_gallery(request, pk):

    provider = ProviderProfile.objects.get(user=request.user)

    service = Service.objects.get(
        id=pk,
        provider=provider
    )

    # Get all service images
    images = service.images.all()

    # Upload new images
    if request.method == "POST":

        uploaded_images = request.FILES.getlist("images")

        for img in uploaded_images:
            ServiceGallery.objects.create(
                service=service,
                image=img
            )

        messages.success(request, "Images uploaded successfully.")

        return redirect("service_gallery", pk=service.id)

    context = {
        "service": service,
        "images": images
    }

    return render(
        request,
        "providers/services/service_gallery.html",
        context
    )


from bookings.models import Booking


@login_required
def provider_bookings(request):

    provider = ProviderProfile.objects.get(user=request.user)

    bookings = Booking.objects.filter(
        provider=provider
    ).order_by("-created_at")

    context = {
        "bookings": bookings
    }

    return render(
        request,
        "providers/bookings.html",
        context
    )


@login_required
def booking_status_update(request, booking_id, status):

    provider = ProviderProfile.objects.get(user=request.user)

    booking = Booking.objects.get(
        booking_id=booking_id,
        provider=provider
    )

    booking.status = status
    booking.save()

    messages.success(request, "Booking updated successfully")

    return redirect("provider_bookings")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from reviews.models import Review
from services.models import Service
from django.db.models import Avg

@login_required
def provider_reviews(request):

    # Get provider services
    services = Service.objects.filter(provider__user=request.user)

    # Get reviews for those services
    reviews = Review.objects.filter(service__in=services).select_related("user", "service")

    # Stats
    total_reviews = reviews.count()
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    context = {
        "reviews": reviews,
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
    }

    return render(request, "providers/reviews.html", context)