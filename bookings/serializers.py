from rest_framework import serializers
from .models import Booking
from tours.models import Tour
from tours.serializers import TourSerializer
from reviews.models import Review

class BookingSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), write_only=True, source='tour')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    can_review = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'tour', 'tour_id', 'start_date', 'end_date', 'status', 'total_price', 'created_at', 'user', 'hotel', 'can_review']
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        tour = data.get('tour')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date:
            days = (end_date - start_date).days
            if days != tour.duration_days:
                raise serializers.ValidationError(
                    f"Длительность тура составляет {tour.duration_days} дней. Вы выбрали {days} дней."
                )
        return data

    def create(self, validated_data):
        tour = validated_data['tour']
        validated_data['total_price'] = tour.price
        return super().create(validated_data)
    
    def get_can_review(self, obj):
        user = self.context["request"].user

        if obj.status != "completed":
            return False

        if obj.tour:
            return not Review.objects.filter(user=user, tour=obj.tour).exists()

        if obj.hotel:
            return not Review.objects.filter(user=user, hotel=obj.hotel).exists()

        return False