from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Booking
from services.models import Service
from providers.models import ProviderProfile

from datetime import date
from datetime import date
from django.contrib import messages

@login_required
def create_booking(request, service_id):

    service = get_object_or_404(Service, id=service_id)
    provider = service.provider

    if request.method == "POST":

        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        quantity = int(request.POST.get("quantity") or 1)
        phone = request.POST.get("phone")
        special_request = request.POST.get("special_request")

        # Convert to date
        check_in_date = None
        check_out_date = None

        if check_in:
            check_in_date = date.fromisoformat(check_in)

        if check_out:
            check_out_date = date.fromisoformat(check_out)

        # ❗ Validation 1: Past date
        if check_in_date and check_in_date < date.today():
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect("create_booking", service_id=service.id)

        # ❗ Validation 2: Checkout before checkin
        if check_in_date and check_out_date and check_out_date <= check_in_date:
            messages.error(request, "Check-out must be after check-in date.")
            return redirect("create_booking", service_id=service.id)

        booking = Booking.objects.create(
            user=request.user,
            provider=provider,
            service=service,
            check_in=check_in_date,
            check_out=check_out_date,
            quantity=quantity,
            phone=phone,
            special_request=special_request
        )

        messages.success(request, f"Booking created successfully. ID: {booking.booking_id}")

        return redirect("my_bookings")

    

    return render(request, "users/book_service.html", {
        "service": service,
        "today": date.today()
    })

@login_required
def booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    return render(request, "users/booking_details.html", {
        "booking": booking
    })