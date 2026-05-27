"""
Scheduled notification jobs.

In development: run manually via management command or Django shell.
In production: wire these functions to Celery Beat tasks.

Example Celery task::

    from celery import shared_task
    from notifications.cron import send_inactivity_reminders

    @shared_task
    def inactivity_reminder_task():
        send_inactivity_reminders()
"""

from datetime import timedelta

from django.utils import timezone

from notifications.models import Notification
from sessions.models import WorkoutSession
from users.models import User


def send_inactivity_reminders():
    """Notify users who haven't logged a session in 7 days."""
    cutoff = timezone.now() - timedelta(days=7)
    inactive_users = User.objects.exclude(
        id__in=WorkoutSession.objects.filter(start_time__gte=cutoff).values("user_id")
    )
    count = 0
    for user in inactive_users:
        Notification.objects.create(
            user=user,
            type="reminder",
            title="Miss you! Time to train",
            message="It has been a while since your last session. Let's get moving!",
        )
        count += 1
    return count
