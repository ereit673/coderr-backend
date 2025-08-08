from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds a 'type' field to categorize users as either 'business' or 'customer'.
    Ensures 'username' and 'email' are unique identifiers.

    Fields:
        - username: Unique username for authentication.
        - email: Unique email address.
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


class Profile(models.Model):
    """
    User profile model linked to CustomUser.

    Contains additional user information such as name, contact details,
    and profile picture. Automatically creates a profile when a user is created.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(
        max_length=30, blank=True, null=False, default='')
    last_name = models.CharField(
        max_length=30, blank=True, null=False, default='')
    file = models.FileField(upload_to='profiles/', blank=True, null=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(
        max_length=255, blank=True, null=False, default='')
    tel = models.CharField(max_length=15, blank=True, null=False, default='')
    description = models.TextField(blank=True, null=False, default='')
    working_hours = models.CharField(
        max_length=50, blank=True, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        """        
        Override save method to set uploaded_at field when the profile is saved.

        If the profile already exists, check if the file has changed and update
        the uploaded_at timestamp accordingly.
        """

        if self.pk:
            old_file = Profile.objects.get(pk=self.pk).file
            if old_file != self.file:
                self.uploaded_at = timezone.now()
        else:
            if self.file is not None:
                self.uploaded_at = timezone.now()
            else:
                self.uploaded_at = None

        super().save(*args, **kwargs)
