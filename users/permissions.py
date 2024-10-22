from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователей группы Moderator."""

    def has_permission(self, request, view):
        """Проверяет состоит ли пользователь в группе Moderator."""
        return request.user.groups.filter(name="moderator").exists()
