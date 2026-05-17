from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        tour = data.get("tour")
        hotel = data.get("hotel")

        if not tour and not hotel:
            raise serializers.ValidationError("Нужно указать тур или отель")

        if tour and hotel:
            raise serializers.ValidationError("Нельзя оба сразу")

        return data