from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerAdminModeratorToEdit(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role in ["moderator", "admin"] or request.user.is_superuser:
            return True
        return request.user == obj.author
