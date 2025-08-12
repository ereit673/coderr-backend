from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Permission to only allow customer users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsReviewer(BasePermission):
    """
    Permission to only allow the reviewer of a review to access certain views.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.reviewer
