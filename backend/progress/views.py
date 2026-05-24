from rest_framework import permissions, viewsets

from api.permissions import IsOwner
from progress.models import ProgressEntry
from progress.serializers import ProgressEntrySerializer


class ProgressEntryViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProgressEntry.objects.filter(user=self.request.user).order_by(
            "-recorded_at"
        )

    def get_permissions(self):
        if self.action in ["destroy", "retrieve", "update", "partial_update"]:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
