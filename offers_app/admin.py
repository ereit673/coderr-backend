from django.contrib import admin

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order

# Register your models here.


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
    list_display = ('id', 'title', 'offer', 'price', 'delivery_time_in_days',
                    'features', 'offer_type')
    search_fields = ('offer__title', 'features')


class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for the Order model.
    """
    list_display = ('id', 'customer_user', 'business_user', 'offer', 'status')


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
admin.site.register(Order, OrderAdmin)
