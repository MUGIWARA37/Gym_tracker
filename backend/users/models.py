import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    FITNESS_GOALS = [
        ("lose_weight", "Lose weight"),
        ("build_muscle", "Build muscle"),
        ("maintain", "Maintain"),
        ("strength", "Strength"),
        ("cardio", "Cardio"),
    ]
    ROLES = [
        ("user", "User"),
        ("coach", "Coach"),
        ("admin", "Admin"),
    ]

    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fitness_goal = models.CharField(max_length=30, choices=FITNESS_GOALS, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} reset token"
