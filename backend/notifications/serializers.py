from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    notification_type = serializers.CharField(source="type", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "title", "message", "type", "notification_type", "is_read", "created_at"]
        read_only_fields = ["id", "created_at"]
