from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import PasswordResetToken, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "profile_picture",
                    "age",
                    "height_cm",
                    "weight_kg",
                    "fitness_goal",
                    "role",
                )
            },
        ),
    )


admin.site.register(PasswordResetToken)
