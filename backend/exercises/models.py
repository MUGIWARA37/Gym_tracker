from django.conf import settings
from django.db import models


class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ("chest", "Chest"),
        ("back", "Back"),
        ("legs", "Legs"),
        ("shoulders", "Shoulders"),
        ("arms", "Arms"),
        ("core", "Core"),
        ("full_body", "Full body"),
    ]
    DIFFICULTIES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUPS)
    equipment_needed = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(max_length=15, choices=DIFFICULTIES)
    calories_burn_estimate = models.PositiveIntegerField(
        help_text="kcal per 30 min, 70kg person"
    )
    met_value = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=4.0,
        help_text="Metabolic Equivalent of Task",
    )
    video_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="exercises/", null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
