from rest_framework import serializers
from .models import Tour, TourImage
from hotels.serializers import HotelSerializer

class TourImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = TourImage
        fields = ["id", "image", "is_main", "order", "url"]

    def get_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

class TourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, read_only=True)
    hotels = HotelSerializer(many=True, read_only=True)
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = "__all__"

    def get_preview_image(self, obj):
        request = self.context.get('request')
        main = obj.images.filter(is_main=True).first()
        if main:
            if request:
                return request.build_absolute_uri(main.image.url)
            return main.image.url
        first = obj.images.first()
        if first:
            if request:
                return request.build_absolute_uri(first.image.url)
            return first.image.url
        return None