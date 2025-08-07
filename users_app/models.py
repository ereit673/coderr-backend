from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds a 'type' field to categorize users as either 'business' or 'customer'.
    Ensures 'username' and 'email' are unique identifiers.

    Fields:
        - username: Unique username for authentication.
        - email: Unique email address for contact and login.
        - type: Specifies the user category; must be 'business' or 'customer'.
    """
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.username
