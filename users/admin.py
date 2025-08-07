from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.
    This allows for additional fields and methods in the future.
    """
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('type',)}),
    )
    list_display = UserAdmin.list_display + ('type', )
