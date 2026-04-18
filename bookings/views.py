from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Booking
from services.models import Service
from providers.models import ProviderProfile
from datetime import date



# from datetime import date
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from bookings.models import Booking
# from services.models import Service


@login_required
def create_booking(request, service_id):

    service = get_object_or_404(Service, id=service_id)
    provider = service.provider

    # 🔥 AUTO DETECT BOOKING TYPE (FIXED)
    main_category = service.subcategory.main_category.name

    if main_category == "Accommodation":
        booking_type = "stay"

    elif main_category == "Food & Dining":
        booking_type = "timeslot"

    elif main_category == "Transport":
        booking_type = "ride"

    else:
        booking_type = "event"


    if request.method == "POST":

        quantity = int(request.POST.get("quantity") or 1)
        phone = request.POST.get("phone")
        special_request = request.POST.get("special_request")

        check_in_date = None
        check_out_date = None

        # 🔥 HANDLE BOOKING TYPES

        if booking_type == "stay":

            check_in = request.POST.get("check_in")
            check_out = request.POST.get("check_out")

            if check_in:
                check_in_date = date.fromisoformat(check_in)

            if check_out:
                check_out_date = date.fromisoformat(check_out)

            if check_in_date and check_in_date < date.today():
                messages.error(request, "Check-in date cannot be in the past.")
                return redirect("create_booking", service_id=service.id)

            if check_in_date and check_out_date and check_out_date < check_in_date:
                messages.error(request, "Check-out cannot be before check-in date.")
                return redirect("create_booking", service_id=service.id)


        elif booking_type == "timeslot":

            booking_date = request.POST.get("date")

            if booking_date:
                check_in_date = date.fromisoformat(booking_date)
                check_out_date = check_in_date

            if check_in_date and check_in_date < date.today():
                messages.error(request, "Booking date cannot be in the past.")
                return redirect("create_booking", service_id=service.id)


        elif booking_type == "ride":

            pickup_date = request.POST.get("pickup_date")

            if pickup_date:
                check_in_date = date.fromisoformat(pickup_date)
                check_out_date = check_in_date


        else:  # event

            booking_date = request.POST.get("date")

            if booking_date:
                check_in_date = date.fromisoformat(booking_date)
                check_out_date = check_in_date


        # ✅ CREATE BOOKING
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
        "booking_type": booking_type,   # ✅ CORRECT VALUE NOW
        "today": date.today()
    })


@login_required
def booking_details(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    # 🔥 AUTO UPDATE STATUS → COMPLETED
    from datetime import date

    if booking.check_out and booking.check_out < date.today():
        if booking.status == "confirmed":
            booking.status = "completed"
            booking.save()

    return render(request, "users/booking_details.html", {
        "booking": booking
    })