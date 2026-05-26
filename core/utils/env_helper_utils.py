import os


def get_bool_env(var_name: str, default: bool = False) -> bool:
    """
    Safely converts an environment variable to a boolean.

    Accepted truthy values:
    - "true"
    - "1"
    - "yes"

    Case-insensitive comparison is used.

    Args:
        var_name: Environment variable name.
        default: Default value if variable is not set.

    Returns:
        Boolean representation of the environment variable.
    """
    value = os.getenv(var_name, str(default))
    return value.lower() in ('true', '1', 'yes')


def get_int_env(var_name: str, default: int) -> int:
    """
    Safely converts an environment variable to an integer.

    If conversion fails, the default value is returned.

    Args:
        var_name: Environment variable name.
        default: Fallback integer value.

    Returns:
        Parsed integer or default.
    """
    try:
        return int(os.getenv(var_name, default))
    except (ValueError, TypeError):
        print(f"Warning: Invalid integer for {var_name}, using default: {default}")
        return default


def get_list_env(var_name: str, default: list = None) -> list:
    """
    Converts a comma-separated environment variable into a list.

    Empty values are ignored.

    Args:
        var_name: Environment variable name.
        default: Default list if variable is missing or empty.

    Returns:
        List of parsed string values.
    """
    if default is None:
        default = []

    value = os.getenv(var_name, '')
    if not value:
        return default

    return [item.strip() for item in value.split(',') if item.strip()]