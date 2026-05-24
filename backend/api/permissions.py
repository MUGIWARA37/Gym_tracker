from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level: obj.user == request.user."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", None) == request.user or getattr(
            obj, "created_by", None
        ) == request.user


class IsOwnerOrAdmin(BasePermission):
    """obj.created_by == request.user or request.user.role == 'admin'."""

    def has_object_permission(self, request, view, obj):
        return (
            getattr(obj, "created_by", None) == request.user
            or getattr(obj, "user", None) == request.user
            or getattr(request.user, "role", "") == "admin"
        )


class IsOwnerOrCoach(BasePermission):
    """Owner OR any user with role == 'coach' or 'admin'."""

    def has_object_permission(self, request, view, obj):
        return (
            getattr(obj, "created_by", None) == request.user
            or getattr(obj, "user", None) == request.user
            or getattr(request.user, "role", "") in ("coach", "admin")
        )


class IsCoachOrAdmin(BasePermission):
    """request.user.role in ('coach', 'admin')."""

    def has_permission(self, request, view):
        return getattr(request.user, "role", "") in ("coach", "admin")
