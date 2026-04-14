from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Review
from services.models import Service
from bookings.models import Booking


@login_required
def add_review(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    # 🔒 ONLY COMPLETED BOOKINGS
    has_completed = Booking.objects.filter(
        user=request.user,
        service=service,
        status="completed"
    ).exists()

    if not has_completed:
        messages.error(request, "You must complete booking to review.")
        return redirect("service_details", service_id=service.id)

    review = Review.objects.filter(
        user=request.user,
        service=service
    ).first()

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating:
            messages.error(request, "Select rating")
            return redirect("service_details", service_id=service.id)

        # ✏️ EDIT if exists
        if review:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, "Review updated successfully!")
        else:
            Review.objects.create(
                user=request.user,
                service=service,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Review added successfully!")

    return redirect("service_details", service_id=service.id)


@login_required
def delete_review(request, service_id):

    review = get_object_or_404(
        Review,
        user=request.user,
        service_id=service_id
    )

    review.delete()

    messages.success(request, "Review deleted successfully!")

    return redirect("service_details", service_id=service_id)