from django.utils import timezone
from rest_framework import serializers

from sessions.models import ExerciseLog, WorkoutSession


class ExerciseLogSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source="exercise.name", read_only=True)
    muscle_group = serializers.CharField(source="exercise.muscle_group", read_only=True)

    class Meta:
        model = ExerciseLog
        fields = [
            "id",
            "session",
            "exercise",
            "exercise_name",
            "muscle_group",
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
    workout_plan_name = serializers.SerializerMethodField()
    mood_display = serializers.CharField(source="get_mood_display", read_only=True)

    class Meta:
        model = WorkoutSession
        fields = [
            "id",
            "user",
            "workout_plan",
            "workout_plan_name",
            "start_time",
            "end_time",
            "calories_burned",
            "notes",
            "mood",
            "mood_display",
            "completed",
            "logs",
        ]
        read_only_fields = ["id", "user", "calories_burned"]

    def get_workout_plan_name(self, obj):
        if obj.workout_plan:
            return obj.workout_plan.title
        return None

    def update(self, instance, validated_data):
        was_completed = instance.completed
        instance = super().update(instance, validated_data)
        if instance.completed and not was_completed and instance.end_time is None:
            instance.end_time = timezone.now()
            instance.save(update_fields=["end_time"])
        return instance
