from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from bookings.models import Booking
from categories.models import MainCategory, SubCategory


@login_required
def user_dashboard(request):

    user = request.user

    bookings = Booking.objects.filter(user=user).select_related(
        "service", "provider"
    )

    total_bookings = bookings.count()

    upcoming_trips = bookings.filter(status="confirmed").count()

    completed_trips = bookings.filter(status="completed").count()

    recent_bookings = bookings.order_by("-created_at")[:5]

    categories = MainCategory.objects.filter(is_active=True)

    context = {
        "total_bookings": total_bookings,
        "upcoming_trips": upcoming_trips,
        "completed_trips": completed_trips,
        "recent_bookings": recent_bookings,
        "categories": categories
    }

    return render(request, "users/dashboard.html", context)

def explore_category(request, category_id):

    category = MainCategory.objects.get(id=category_id)

    subcategories = SubCategory.objects.filter(main_category=category)

    context = {
        "category": category,
        "subcategories": subcategories
    }

    return render(request, "users/explore_category.html", context)






from services.models import Service
from categories.models import SubCategory


def services_by_subcategory(request, subcategory_id):

    subcategory = SubCategory.objects.get(id=subcategory_id)

    services = Service.objects.filter(
        subcategory=subcategory,
        is_available=True
    ).select_related("provider")

    return render(request, "users/services_list.html", {
        "subcategory": subcategory,
        "services": services
    })


from services.models import Service
from django.shortcuts import render, get_object_or_404


def service_details(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    images = service.images.all()

    return render(request, "users/service_details.html", {
        "service": service,
        "images": images
    })


from bookings.models import Booking


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "users/my_bookings.html", {
        "bookings": bookings
    })


from django.shortcuts import get_object_or_404
from bookings.models import Booking
from django.contrib import messages


@login_required
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    if booking.status == "pending":
        booking.status = "cancelled"
        booking.save()

        messages.success(request, "Booking cancelled successfully.")

    else:
        messages.error(request, "You cannot cancel this booking.")

    return redirect("my_bookings")