from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from bookings.models import Booking
from categories.models import MainCategory, SubCategory
from reviews.models import Review
from django.db.models import Avg
from bookings.models import Booking
from services.models import Service




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

    # ⭐ NEW: Top Rated Services
    top_services = Service.objects.filter(
        is_available=True
    ).annotate(
        avg_rating=Avg("reviews__rating")
    ).order_by("-avg_rating")[:6]

    context = {
        "total_bookings": total_bookings,
        "upcoming_trips": upcoming_trips,
        "completed_trips": completed_trips,
        "recent_bookings": recent_bookings,
        "categories": categories,

        # ⭐ ADD THIS
        "top_services": top_services,
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

def services_by_subcategory(request, subcategory_id):

    subcategory = SubCategory.objects.get(id=subcategory_id)

    sort = request.GET.get("sort")

    services = Service.objects.filter(
        subcategory=subcategory,
        is_available=True
    ).select_related("provider").annotate(
        avg_rating=Avg("reviews__rating")
    )

    # 🔽 SORTING LOGIC
    if sort == "price_low":
        services = services.order_by("price")

    elif sort == "price_high":
        services = services.order_by("-price")

    elif sort == "rating":
        services = services.order_by("-avg_rating")

    elif sort == "new":
        services = services.order_by("-created_at")

    return render(request, "users/services_list.html", {
        "subcategory": subcategory,
        "services": services,
        "selected_sort": sort
    })

from services.models import Service
from django.shortcuts import render, get_object_or_404




from datetime import date
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

def service_details(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    # 🔥 AUTO UPDATE → COMPLETED (VERY IMPORTANT)
    if request.user.is_authenticated:
        Booking.objects.filter(
            user=request.user,
            service=service,
            check_out__lt=date.today(),
            status="confirmed"
        ).update(status="completed")

    reviews = Review.objects.filter(service=service)

    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    has_booked = False
    user_reviewed = False
    user_review = None

    if request.user.is_authenticated:

        # 🔒 ONLY COMPLETED BOOKINGS
        has_booked = Booking.objects.filter(
            user=request.user,
            service=service,
            status="completed"
        ).exists()

        # ⭐ Get user's review
        user_review = Review.objects.filter(
            user=request.user,
            service=service
        ).first()

        if user_review:
            user_reviewed = True

    images = service.images.all()

    context = {
        "service": service,
        "images": images,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "has_booked": has_booked,
        "user_reviewed": user_reviewed,
        "user_review": user_review,
    }

    return render(request, "users/service_details.html", context)
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


