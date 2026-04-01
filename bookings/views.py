from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        booking.status = "cancelled"
        booking.save()

        return Response({"status": "cancelled"})

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        if booking.status != "pending":
            return Response({"error": "Booking cannot be paid (status is not pending)"}, status=400)

        card_number = request.data.get("card_number")
        expiry = request.data.get("expiry")
        cvv = request.data.get("cvv")

        if not all([card_number, expiry, cvv]):
            return Response({"error": "Payment details required"}, status=400)

        import time; time.sleep(1)

        booking.status = "confirmed"
        booking.save()

        # Возвращаем обновлённую информацию о бронировании
        serializer = self.get_serializer(booking)
        return Response(serializer.data)