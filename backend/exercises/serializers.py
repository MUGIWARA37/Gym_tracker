from django.conf import settings
from rest_framework import serializers

from api.validators import validate_image_upload
from exercises.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "description",
            "muscle_group",
            "equipment_needed",
            "difficulty_level",
            "calories_burn_estimate",
            "met_value",
            "video_url",
            "image",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_image(self, value):
        if value is None:
            return value
        return validate_image_upload(value, settings.MAX_UPLOAD_SIZE_MB)
