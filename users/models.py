from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This allows for additional fields and methods in the future.
    """
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.username
