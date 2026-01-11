from rest_framework.exceptions import ValidationError


def validate_passwords_match(password1: str, password2: str, field_name: str = 'confirm_password') -> None:
    """
    Validates that two passwords match.
    Raises serializers.ValidationError if invalid.
    """
    if password1 != password2:
        raise ValidationError({field_name: 'Passwords do not match.'})
