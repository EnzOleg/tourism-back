from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    tour = models.ForeignKey(
        "tours.Tour",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rating = models.IntegerField()
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id}"
    
    def clean(self):
        if not self.tour and not self.hotel:
            raise ValidationError("Отзыв должен быть либо к туру, либо к отелю")

        if self.tour and self.hotel:
            raise ValidationError("Нельзя оставлять отзыв одновременно к туру и отелю")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tour"],
                name="unique_user_tour_review"
            ),
            models.UniqueConstraint(
                fields=["user", "hotel"],
                name="unique_user_hotel_review"
            ),
        ]
