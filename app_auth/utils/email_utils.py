def get_email_local_part(value: str) -> str:
    """
    Extracts the local part (before '@') from an email address.

    If the input is not a valid string or does not contain '@',
    the original value is returned unchanged.

    Args:
        value: Email address string.

    Returns:
        Local part of the email (trimmed) or original value if invalid.
    """
    if not isinstance(value, str) or '@' not in value:
        return value
    return value.split('@', 1)[0].strip()