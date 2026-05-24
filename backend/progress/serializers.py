from django.conf import settings
from rest_framework import serializers

from api.validators import validate_image_upload
from progress.models import ProgressEntry


class ProgressEntrySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = ProgressEntry
        fields = [
            "id",
            "user",
            "weight_kg",
            "body_fat_percentage",
            "chest_cm",
            "waist_cm",
            "arm_cm",
            "leg_cm",
            "photo",
            "recorded_at",
        ]
        read_only_fields = ["id", "user", "recorded_at"]

    def validate_photo(self, value):
        if value is None:
            return value
        return validate_image_upload(value, settings.MAX_UPLOAD_SIZE_MB)
