from rest_framework.exceptions import ValidationError


def validate_passwords_match(password1: str, password2: str, field_name: str = 'confirm_password') -> None:
    """
    Validates that two password inputs are identical.

    Intended for use in serializers or form validation where a password
    confirmation field is required.

    Args:
        password1: Primary password value.
        password2: Confirmation password value.
        field_name: Field name used in the validation error response.

    Raises:
        ValidationError: If the passwords do not match.
    """
    if password1 != password2:
        raise ValidationError({field_name: 'Passwords do not match.'})