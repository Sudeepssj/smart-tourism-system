from django.db import models
from providers.models import ProviderProfile
from categories.models import SubCategory


# ----------------------------
# SERVICE MODEL
# ----------------------------
class Service(models.Model):

    # 🔥 NEW FIELD (ADD THIS ABOVE provider OR BELOW — ANYWHERE INSIDE MODEL)
    BOOKING_TYPE_CHOICES = [
        ("stay", "Stay (Hotel/Resort)"),
        ("timeslot", "Time Slot (Cafe/Food)"),
        ("ride", "Ride (Transport)"),
        ("event", "Event (Tours/Activities)"),
    ]

    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPE_CHOICES,
        default="event"
    )

    # EXISTING FIELDS (NO CHANGE)
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="services"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="services"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Availability
    is_available = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ----------------------------
# SERVICE GALLERY
# ----------------------------
class ServiceGallery(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="service_gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.service.title}"