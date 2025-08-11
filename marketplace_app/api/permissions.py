from rest_framework.permissions import BasePermission


class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user
