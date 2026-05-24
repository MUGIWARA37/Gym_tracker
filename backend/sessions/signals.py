from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from notifications.models import Notification
from sessions.models import WorkoutSession
from sessions.services import calculate_calories


@receiver(pre_save, sender=WorkoutSession)
def cache_previous_completion(sender, instance, **kwargs):
    if instance.pk:
        instance._was_completed = (
            WorkoutSession.objects.filter(pk=instance.pk)
            .values_list("completed", flat=True)
            .first()
        )
    else:
        instance._was_completed = False


@receiver(post_save, sender=WorkoutSession)
def session_completed(sender, instance, created, **kwargs):
    if instance.completed and not getattr(instance, "_was_completed", False):
        calculate_calories(instance)
        Notification.objects.create(
            user=instance.user,
            type="achievement",
            title="Workout complete! 🎯",
            message="Great job finishing your workout session!",
        )
