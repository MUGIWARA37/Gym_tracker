from django.urls import include, path
from rest_framework.routers import DefaultRouter

from exercises.views import ExerciseViewSet
from notifications.views import NotificationViewSet
from nutrition.views import NutritionGoalView
from progress.views import ProgressEntryViewSet
from sessions.views import WorkoutSessionViewSet
from users.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    ProfileView,
    RegisterView,
    TokenRefreshView,
)
from workouts.views import WorkoutPlanViewSet
from .views import DashboardStatsView

router = DefaultRouter()
router.register("exercises", ExerciseViewSet, basename="exercise")
router.register("workout-plans", WorkoutPlanViewSet, basename="workout-plan")
router.register("sessions", WorkoutSessionViewSet, basename="session")
router.register("progress", ProgressEntryViewSet, basename="progress")
router.register("notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("nutrition/", NutritionGoalView.as_view(), name="nutrition-goal"),
    path(
        "auth/",
        include(
            [
                path("register/", RegisterView.as_view(), name="auth-register"),
                path("login/", LoginView.as_view(), name="auth-login"),
                path(
                    "token/refresh/",
                    TokenRefreshView.as_view(),
                    name="auth-token-refresh",
                ),
                path("logout/", LogoutView.as_view(), name="auth-logout"),
                path("profile/", ProfileView.as_view(), name="auth-profile"),
                path(
                    "password/reset/",
                    PasswordResetRequestView.as_view(),
                    name="auth-password-reset",
                ),
                path(
                    "password/reset/confirm/",
                    PasswordResetConfirmView.as_view(),
                    name="auth-password-reset-confirm",
                ),
            ]
        ),
    ),
]
