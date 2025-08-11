from rest_framework.permissions import BasePermission


class IsBusiness(BasePermission):
    """
    Permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'


class IsCustomer(BasePermission):
    """
    Permission to only allow customer users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsOfferOwner(BasePermission):
    """
    Permission to only allow the owner of an offer to access certain views.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user
