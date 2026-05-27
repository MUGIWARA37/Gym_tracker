from datetime import timedelta

from django.utils import timezone
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sessions.models import WorkoutSession


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        week_start = now - timedelta(days=7)
        sessions = WorkoutSession.objects.filter(user=request.user)
        weekly_sessions = sessions.filter(start_time__gte=week_start).count()
        weekly_calories = (
            sessions.filter(start_time__gte=week_start, completed=True)
            .values_list("calories_burned", flat=True)
            .order_by()
        )
        weekly_calories_burned = round(sum(weekly_calories) or 0, 2)
        current_streak_days = _calculate_streak_days(sessions)
        goal_completion_percent = _calculate_goal_completion(sessions, week_start)
        from sessions.serializers import WorkoutSessionSerializer
        recent_qs = sessions.order_by("-start_time").select_related("workout_plan")[:5]
        recent_sessions = WorkoutSessionSerializer(recent_qs, many=True).data
        muscle_group_distribution = _muscle_group_distribution(request.user, week_start)

        from exercises.models import Exercise
        return Response(
            {
                "weekly_sessions": weekly_sessions,
                "weekly_calories_burned": weekly_calories_burned,
                "current_streak_days": current_streak_days,
                "goal_completion_percent": goal_completion_percent,
                "recent_sessions": recent_sessions,
                "muscle_group_distribution": muscle_group_distribution,
                "total_exercises": Exercise.objects.count(),
            }
        )


def _calculate_streak_days(sessions_queryset):
    completed_dates = (
        sessions_queryset.filter(completed=True)
        .order_by("-start_time")
        .values_list("start_time", flat=True)
    )
    unique_dates = []
    for start_time in completed_dates:
        date_value = start_time.date()
        if not unique_dates or unique_dates[-1] != date_value:
            unique_dates.append(date_value)

    if not unique_dates:
        return 0

    streak = 0
    cursor = timezone.now().date()
    for date_value in unique_dates:
        if date_value == cursor or date_value == cursor - timedelta(days=1):
            streak += 1
            cursor = date_value - timedelta(days=1)
            continue
        break
    return streak


def _calculate_goal_completion(sessions_queryset, week_start):
    completed = sessions_queryset.filter(start_time__gte=week_start, completed=True).count()
    target = 5
    return min(round((completed / target) * 100), 100)


def _muscle_group_distribution(user, week_start):
    from exercises.models import Exercise
    from sessions.models import ExerciseLog

    logs = ExerciseLog.objects.filter(
        session__user=user, session__start_time__gte=week_start, completed=True
    )
    counts = (
        logs.values("exercise__muscle_group")
        .order_by()
        .annotate(total=models.Count("id"))
    )
    distribution = {item["exercise__muscle_group"]: item["total"] for item in counts}
    if not distribution:
        distribution = {group[0]: 0 for group in Exercise.MUSCLE_GROUPS}
    return distribution
