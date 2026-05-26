from django.conf import settings
from django.db import models

from exercises.models import Exercise


class WorkoutPlan(models.Model):
    FITNESS_GOALS = [
        ("lose_weight", "Lose weight"),
        ("build_muscle", "Build muscle"),
        ("maintain", "Maintain"),
        ("strength", "Strength"),
        ("cardio", "Cardio"),
    ]
    DIFFICULTIES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]
    DAYS_PER_WEEK_CHOICES = [(4, "4 days"), (5, "5 days"), (6, "6 days")]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=30, choices=FITNESS_GOALS)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTIES)
    days_per_week = models.PositiveSmallIntegerField(
        choices=DAYS_PER_WEEK_CHOICES, default=4
    )
    estimated_duration = models.PositiveIntegerField(help_text="minutes")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    # Generated metadata (kept as JSON for easy iteration on templates).
    structure = models.JSONField(blank=True, default=dict)
    nutrition_guidance = models.JSONField(blank=True, default=dict)

    exercises = models.ManyToManyField(
        Exercise, through="WorkoutPlanExercise", related_name="plans"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WorkoutPlanExercise(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(default=1, help_text="Day number in the plan")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    sets = models.PositiveSmallIntegerField(default=3)
    reps = models.PositiveSmallIntegerField(default=10)
    rest_time_seconds = models.PositiveIntegerField(default=60)

    class Meta:
        ordering = ["day", "order"]
        unique_together = ["plan", "day", "order"]

    def __str__(self):
        return f"{self.plan.title} (Day {self.day}) - {self.exercise.name}"
