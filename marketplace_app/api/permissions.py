from rest_framework.permissions import BasePermission


class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has a business profile
        return request.user.is_authenticated and request.user.type == 'business'


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user
