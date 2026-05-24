from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsOwner, IsOwnerOrCoach
from sessions.models import ExerciseLog, WorkoutSession
from sessions.serializers import ExerciseLogSerializer, WorkoutSessionSerializer


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ["start_time", "end_time"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", "") in ("coach", "admin"):
            return WorkoutSession.objects.all().order_by("-start_time")
        return WorkoutSession.objects.filter(user=user).order_by("-start_time")

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsOwnerOrCoach()]
        if self.action in ["update", "partial_update", "destroy", "logs", "update_log"]:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="logs")
    def logs(self, request, pk=None):
        serializer = ExerciseLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(session=self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="logs/(?P<log_id>[^/.]+)")
    def update_log(self, request, pk=None, log_id=None):
        log = ExerciseLog.objects.filter(id=log_id, session_id=pk).first()
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExerciseLogSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
