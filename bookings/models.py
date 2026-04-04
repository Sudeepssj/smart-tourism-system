from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from providers.models import ProviderProfile


class Booking(models.Model):

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="provider_bookings"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_bookings"
    )

    check_in = models.DateField(null=True, blank=True)

    check_out = models.DateField(null=True, blank=True)

    booking_date = models.DateField(null=True, blank=True)

    quantity = models.PositiveIntegerField()

    phone = models.CharField(max_length=15)

    special_request = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("rejected", "Rejected"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_id

    def save(self, *args, **kwargs):

        if not self.booking_id:

            last_booking = Booking.objects.order_by("id").last()

            if last_booking:
                last_id = int(last_booking.booking_id.split("-")[1])
                new_id = last_id + 1
            else:
                new_id = 1001

            self.booking_id = f"ST-{new_id}"

        super().save(*args, **kwargs)