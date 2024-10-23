from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователей группы Moderator."""

    def has_permission(self, request, view):
        """Проверяет состоит ли пользователь в группе Moderator."""
        return request.user.groups.filter(name="moderator").exists()


class IsOwnerPermission(permissions.BasePermission):
    """Проверка прав доступа для владельцев."""

    def has_object_permission(self, request, view, obj):
        """Проверяет является ли пользователь владельцем."""
        return obj.owner == request.user


class IsUserPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователя."""

    def has_object_permission(self, request, view, obj):
        """Проверяет является ли пользователь объектом."""
        return obj.email == request.user.email
