from datetime import timedelta

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from notifications.models import Notification
from sessions.models import WorkoutSession
from users.models import User


class InactivityReminderCron(CronJobBase):
    RUN_AT_TIMES = ["03:00"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = "notifications.inactivity_reminder"

    def do(self):
        cutoff = timezone.now() - timedelta(days=7)
        inactive_users = User.objects.exclude(
            id__in=WorkoutSession.objects.filter(start_time__gte=cutoff).values("user_id")
        )
        for user in inactive_users:
            Notification.objects.create(
                user=user,
                type="reminder",
                title="Miss you! Time to train",
                message="It has been a while since your last session. Let's get moving!",
            )
