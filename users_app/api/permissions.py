from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own profile.
    Other users can only read the profile.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
