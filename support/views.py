from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import SupportRequest
from .serializers import SupportRequestSerializer


class SupportRequestViewSet(ModelViewSet):
    queryset = SupportRequest.objects.all().order_by("-created_at")
    serializer_class = SupportRequestSerializer
    permission_classes = [AllowAny]