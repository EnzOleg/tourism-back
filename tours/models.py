from django.db import models
from hotels.models import Hotel
from django.db import models

class Tour(models.Model):
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hotels = models.ManyToManyField(Hotel, blank=True, related_name='tours')
    description = models.TextField()

    manager_name = models.CharField(max_length=255, blank=True, null=True)
    manager_phone = models.CharField(max_length=50, blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class TourImage(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to='tour_images/')
    is_main = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.tour.title} image"