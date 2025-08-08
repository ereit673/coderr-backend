from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the CustomUser model.

    Extends Django's UserAdmin to include the 'type' field in the admin interface.
    """
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('type',)}),
    )
    list_display = UserAdmin.list_display + ('type', )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for the Profile model.
    """
    model = Profile
    fieldsets = (
        (None, {
            "fields": (
                'user', 'first_name', 'last_name', 'file',
                'location', 'tel', 'description', 'working_hours'
            ),
        }),
    )
    list_display = (
        'user', 'first_name', 'last_name', 'location', 'tel',
        'description', 'working_hours', 'created_at')
