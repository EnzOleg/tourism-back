from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().select_related("user", "tour", "hotel")
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)