from typing import Dict, Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import PasswordField

from app_auth.models.custom_user import CustomUser
from app_auth.utils.password_utils import validate_passwords_match


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for basic User profile representation.

    Used primarily for displaying non-sensitive user information.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling new user registration.

    Validates email uniqueness, password complexity, and ensures
    that password confirmation matches.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'confirmed_password']
        read_only_fields = ['id']

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email already exists.")]
    )
    password = PasswordField()
    confirmed_password = PasswordField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform cross-field validation for passwords.

        Args:
            attrs (Dict[str, Any]): Dictionary of field values.

        Returns:
            Dict[str, Any]: The validated data with 'confirmed_password' removed.

        Raises:
            ValidationError: If passwords do not match or fail complexity checks.
        """
        validate_passwords_match(attrs['password'], attrs['confirmed_password'])
        validate_password(attrs['password'])
        validated_data = attrs.copy()
        validated_data.pop('confirmed_password')
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Captures credentials required to generate JWT tokens.
    """
    username_field = "email"
    email = serializers.EmailField()
    password = PasswordField()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for updating an existing user's password.

    Validates the new password against matching and complexity rules.
    """
    new_password = PasswordField()
    confirm_password = PasswordField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the new password entries.

        Args:
            attrs (Dict[str, Any]): The password fields to validate.

        Returns:
            Dict[str, Any]: Validated attributes.
        """
        validate_passwords_match(attrs['new_password'], attrs['confirm_password'])
        validate_password(attrs['new_password'])
        return attrs