from django.contrib import admin

from reviews_app.models import Review


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for the Review model.
    """
    list_display = ('id', 'business_user', 'reviewer', 'rating', 'description')


admin.site.register(Review, ReviewAdmin)
