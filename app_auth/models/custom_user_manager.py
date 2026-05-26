from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model where email is the unique identifier.

    This manager overrides the default behavior to ensure that users are created
    using email addresses instead of usernames. It handles normalization and
    standardized validation for user and superuser creation.
    """

    def create_user(self, email: str, password: str, **extra_fields):
        """
        Creates and saves a regular User with the given email and password.

        Args:
            email (str): The unique email address for the user.
            password (str): The raw password for the user.
            **extra_fields: Additional fields to be passed to the user model
                (e.g., first_name, last_name).

        Returns:
            CustomUser: The created user instance.

        Raises:
            ValueError: If the email or password is not provided.
        """
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')

        # Normalizes the email to ensure 'example@DOMAIN.com' becomes 'example@domain.com'
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Creates and saves a Superuser with the given email and password.

        Automatically sets administrative flags to True.

        Args:
            email (str): The unique email address for the superuser.
            password (str): The raw password for the superuser.
            **extra_fields: Additional fields to be passed to the user model.

        Returns:
            CustomUser: The created superuser instance with elevated permissions.
        """
        extra_fields.update(
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        return self.create_user(email, password, **extra_fields)