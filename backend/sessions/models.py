from django.conf import settings
from django.db import models

from exercises.models import Exercise
from workouts.models import WorkoutPlan


class WorkoutSession(models.Model):
    MOODS = [
        ("motivated", "Motivated"),
        ("tired", "Tired"),
        ("excellent", "Excellent"),
        ("average", "Average"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    calories_burned = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    mood = models.CharField(max_length=15, choices=MOODS, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} session {self.start_time}"


class ExerciseLog(models.Model):
    session = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="logs"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight_used_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    duration_seconds = models.PositiveIntegerField(default=0)
    rest_time_seconds = models.PositiveIntegerField(default=60)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.exercise.name} log"
