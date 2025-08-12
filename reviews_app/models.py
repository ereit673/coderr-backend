from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


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
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username}: {self.rating} stars"
