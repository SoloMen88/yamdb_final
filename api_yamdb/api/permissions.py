from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    """Класс прав доступа модератора"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """Класс прав доступа администратора"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class IsModerator(permissions.BasePermission):
    """Класс прав доступа модератора"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_moderator
                or request.user.is_superuser)


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Кастомный класс прав доступа с проверкой на админа/модератора/автора"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator)
