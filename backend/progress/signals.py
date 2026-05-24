from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification
from progress.models import ProgressEntry


@receiver(post_save, sender=ProgressEntry)
def progress_logged(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            type="workout",
            title="Progress logged",
            message="Your progress entry was saved successfully.",
        )
