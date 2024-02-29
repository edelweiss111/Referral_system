from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Пользователь владелец"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
