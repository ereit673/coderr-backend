from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
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


class Review(models.Model):
    """
    Model representing a review left by a customer for a business user.

    Fields:
        - business_user: ForeignKey to the User being reviewed.
        - reviewer: ForeignKey to the User who wrote the review.
        - rating: Rating given by the reviewer (1-5).
        - description: Optional text description of the review.
        - created_at: Timestamp when the review was created.
        - updated_at: Timestamp when the review was last updated.
    """
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_reviews')
    rating = models.PositiveIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username}: {self.rating} stars"
