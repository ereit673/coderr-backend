from django.contrib.auth import get_user_model
from django.db import models

from offers_app.models import OfferDetail

User = get_user_model()


class Order(models.Model):
    """
    Model representing an order placed by a customer for an offer.

    Fields:
        - customer_user: ForeignKey to the User who placed the order.
        - business_user: ForeignKey to the User who owns the offer.
        - offer: ForeignKey to the OfferDetail being ordered.
        - status: Current status of the order (e.g., in progress, completed).
        - created_at: Timestamp when the order was created.
        - updated_at: Timestamp when the order was last updated.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_orders')
    offer = models.ForeignKey(
        OfferDetail, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_user.username} for {self.offer.title} from {self.business_user.username}"
