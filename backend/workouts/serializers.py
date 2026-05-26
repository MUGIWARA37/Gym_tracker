from rest_framework import serializers

from exercises.serializers import ExerciseSerializer
from workouts.models import WorkoutPlan, WorkoutPlanExercise


class WorkoutPlanExerciseSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source="exercise", read_only=True)

    class Meta:
        model = WorkoutPlanExercise
        fields = [
            "id",
            "day",
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
            "days_per_week",
            "estimated_duration",
            "created_by",
            "is_public",
            "structure",
            "nutrition_guidance",
            "created_at",
            "exercises",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class WorkoutPlanWriteSerializer(serializers.ModelSerializer):
    auto_generate = serializers.BooleanField(write_only=True, default=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            "id",
            "title",
            "description",
            "goal",
            "difficulty",
            "days_per_week",
            "estimated_duration",
            "is_public",
            "auto_generate",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        from workouts.generator import generate_plan

        auto_generate = validated_data.pop("auto_generate", True)
        plan = super().create(validated_data)

        if auto_generate:
            generate_plan(plan)
            plan.refresh_from_db()

        # Ensure there is at least a short description.
        if not plan.description:
            plan.description = (
                f"Auto-generated {plan.days_per_week}-day {plan.get_goal_display()} plan "
                f"({plan.get_difficulty_display()})."
            )
            plan.save(update_fields=["description"])

        return plan
