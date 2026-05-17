from rest_framework import serializers
from .models import Booking
from tours.models import Tour
from hotels.models import Hotel
from tours.serializers import TourSerializer
from hotels.serializers import HotelSerializer
from reviews.models import Review


class BookingSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(),
        write_only=True,
        source='tour'
    )

    hotel = HotelSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        write_only=True,
        source='hotel'
    )

    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    can_review = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'tour',
            'tour_id',
            'hotel',
            'hotel_id',
            'start_date',
            'end_date',
            'people_count',
            'status',
            'total_price',
            'refund_message',
            'created_at',
            'user',
            'can_review'
        ]
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        tour = data.get('tour')
        hotel = data.get('hotel')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        people_count = data.get('people_count', 1)


        if not tour:
            raise serializers.ValidationError("Тур обязателен.")

        if not hotel:
            raise serializers.ValidationError("Выберите отель.")

        if hotel not in tour.hotels.all():
            raise serializers.ValidationError(
                "Выбранный отель не относится к данному туру."
            )
        
        if people_count <= 0:
            raise serializers.ValidationError(
                "Количество людей должно быть больше 0."
            )

        if start_date and end_date:
            days = (end_date - start_date).days

            if days <= 0:
                raise serializers.ValidationError(
                    "Дата окончания должна быть позже даты начала."
                )

        return data

    def create(self, validated_data):
        tour = validated_data['tour']
        hotel = validated_data['hotel']
        people_count = validated_data.get('people_count', 1)

        days = (validated_data['end_date'] - validated_data['start_date']).days

        validated_data['total_price'] = (
            tour.price + hotel.price_per_night * days
        ) * people_count

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