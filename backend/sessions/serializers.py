from django.utils import timezone
from rest_framework import serializers

from sessions.models import ExerciseLog, WorkoutSession
from workouts.models import WorkoutPlan


class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = [
            "id",
            "session",
            "exercise",
            "sets",
            "reps",
            "weight_used_kg",
            "duration_seconds",
            "rest_time_seconds",
            "completed",
        ]
        read_only_fields = ["id", "session"]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    logs = ExerciseLogSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = [
            "id",
            "user",
            "workout_plan",
            "start_time",
            "end_time",
            "calories_burned",
            "notes",
            "mood",
            "completed",
            "logs",
        ]
        read_only_fields = ["id", "user", "calories_burned"]

    def update(self, instance, validated_data):
        was_completed = instance.completed
        instance = super().update(instance, validated_data)
        if instance.completed and not was_completed and instance.end_time is None:
            instance.end_time = timezone.now()
            instance.save(update_fields=["end_time"])
        return instance
