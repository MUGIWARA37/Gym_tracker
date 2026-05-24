from django.conf import settings
from django.db import models


class Notification(models.Model):
    NOTIF_TYPES = [
        ("reminder", "Reminder"),
        ("achievement", "Achievement"),
        ("warning", "Warning"),
        ("workout", "Workout"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=15, choices=NOTIF_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
