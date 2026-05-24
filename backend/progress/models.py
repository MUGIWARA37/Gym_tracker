from django.conf import settings
from django.db import models


class ProgressEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    chest_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    waist_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    arm_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    leg_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    photo = models.ImageField(upload_to="progress/", null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} progress"
