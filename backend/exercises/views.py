from rest_framework import permissions, viewsets

from api.permissions import IsOwnerOrAdmin
from exercises.models import Exercise
from exercises.serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all().order_by("-created_at")
    search_fields = ["name", "description"]
    filterset_fields = ["muscle_group", "difficulty_level"]
    ordering_fields = ["created_at", "name"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
