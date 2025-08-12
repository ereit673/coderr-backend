from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Offer(models.Model):
    """
    Model representing an offer made by a business user.

    Fields:
        - user: ForeignKey to the User who created the offer.
        - title: Title of the offer.
        - image: Optional image associated with the offer.
        - description: Detailed description of the offer.
        - created_at: Timestamp when the offer was created.
        - updated_at: Timestamp when the offer was last updated.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer by {self.user.username}: {self.title}"


class OfferDetail(models.Model):
    """
    Model representing details of an offer.

    Fields:
        - offer: ForeignKey to the Offer this detail belongs to.
        - title: Title of the offer detail.
        - revisions: Number of revisions included in the offer.
        - delivery_time_in_days: Estimated delivery time in days.
        - price: Price of the offer detail.
        - features: Additional features included in the offer.
        - offer_type: Type of the offer (e.g., basic, standard, premium).
    """
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(blank=True, null=True, default=list)
    offer_type = models.CharField(
        choices=OFFER_TYPE_CHOICES, max_length=10)

    def __str__(self):
        return f"Detail for {self.offer.title}: {self.title} ({self.offer_type})"
