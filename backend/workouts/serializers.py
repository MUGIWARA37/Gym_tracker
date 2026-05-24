from rest_framework import serializers

from exercises.serializers import ExerciseSerializer
from workouts.models import WorkoutPlan, WorkoutPlanExercise


class WorkoutPlanExerciseSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source="exercise", read_only=True)

    class Meta:
        model = WorkoutPlanExercise
        fields = [
            "id",
            "exercise",
            "exercise_detail",
            "order",
            "sets",
            "reps",
            "rest_time_seconds",
        ]


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutPlanExerciseSerializer(
        source="workoutplanexercise_set", many=True, read_only=True
    )

    class Meta:
        model = WorkoutPlan
        fields = [
            "id",
            "title",
            "description",
            "goal",
            "difficulty",
            "estimated_duration",
            "created_by",
            "is_public",
            "created_at",
            "exercises",
        ]
        read_only_fields = ["id", "created_by", "created_at"]
