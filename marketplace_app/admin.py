from django.contrib import admin

from marketplace_app.models import Offer, OfferDetail


class OfferAdmin(admin.ModelAdmin):
    """
    Admin interface for the Offer model.
    """
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'description')


class OfferDetailAdmin(admin.ModelAdmin):
    """
    Admin interface for the OfferDetail model.
    """
    list_display = ('title', 'offer', 'price', 'delivery_time_in_days',
                    'features', 'offer_type')
    search_fields = ('offer__title', 'features')


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
