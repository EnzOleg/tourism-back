from rest_framework import serializers
from .models import SupportRequest


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = [
            "id",
            "name",
            "phone",
            "message",
            "status",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at"
        ]

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Имя должно содержать минимум 2 символа."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if len(value) < 7:
            raise serializers.ValidationError(
                "Введите корректный номер телефона."
            )

        return value