from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "service")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.service.title} - {self.rating}⭐ by {self.user.username}"