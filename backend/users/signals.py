from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from users.models import User


@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            type="reminder",
            title="Welcome — set your goal",
            message="Welcome to Smart Gym! Update your profile and fitness goal to get started.",
        )
