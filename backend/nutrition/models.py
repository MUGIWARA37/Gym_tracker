from django.conf import settings
from django.db import models


class NutritionGoal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calories_target = models.PositiveIntegerField()
    protein_g = models.PositiveIntegerField()
    carbs_g = models.PositiveIntegerField()
    fats_g = models.PositiveIntegerField()
    water_ml = models.PositiveIntegerField(default=2000)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} nutrition goal"
