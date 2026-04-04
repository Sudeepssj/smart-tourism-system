from django.db import models
from django.contrib.auth.models import User
from locations.models import District
from categories.models import SubCategory


class ProviderProfile(models.Model):

    # --------------------
    # USER LINK
    # --------------------
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --------------------
    # BUSINESS CATEGORY
    # --------------------
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="providers"
    )

    # --------------------
    # BUSINESS BASIC INFO
    # --------------------
    business_name = models.CharField(max_length=150)
    business_description = models.TextField(blank=True)

    logo = models.ImageField(upload_to="provider_logos/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="provider_covers/", blank=True, null=True)

    # --------------------
    # CONTACT INFO
    # --------------------
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)

    business_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # --------------------
    # LOCATION INFO
    # --------------------
    full_address = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    google_map_link = models.URLField(blank=True, null=True)

    # --------------------
    # BUSINESS TIMINGS
    # --------------------
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    # --------------------
    # BUSINESS STATUS
    # --------------------
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    is_active = models.BooleanField(default=True)

    # --------------------
    # RATING (Future use)
    # --------------------
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)

    # --------------------
    # TIMESTAMP
    # --------------------
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name