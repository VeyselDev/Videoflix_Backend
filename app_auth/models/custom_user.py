from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from app_auth.models.custom_user_manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the unique identifier for authentication
    instead of usernames.

    This model extends AbstractBaseUser and PermissionsMixin to integrate
    fully with Django's permission system while allowing for a flexible,
    email-based login.

    Attributes:
        email (EmailField): The primary unique identifier for the user.
        username (CharField): An optional display name or secondary identifier.
        is_active (BooleanField): Designates whether this user account should be
            considered active. Set to False by default for manual/email activation.
        is_staff (BooleanField): Designates whether the user can log into
            this admin site.
        created_at (DateTimeField): Automatically stored timestamp of creation.
        updated_at (DateTimeField): Automatically updated timestamp of last change.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, unique=True, null=True, blank=True, default=None)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    # Configuration for authentication backend
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        """
        Returns the string representation of the user.

        Returns:
            str: The user's email address.
        """
        return self.email

    class Meta:
        """
        Meta options for the CustomUser model.
        """
        ordering = ['-created_at']
        verbose_name = 'User'