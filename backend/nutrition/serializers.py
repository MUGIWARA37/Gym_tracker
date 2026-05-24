from rest_framework import serializers

from nutrition.models import NutritionGoal


class NutritionGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionGoal
        fields = [
            "id",
            "user",
            "calories_target",
            "protein_g",
            "carbs_g",
            "fats_g",
            "water_ml",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "updated_at"]
