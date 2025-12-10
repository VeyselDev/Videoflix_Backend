import os


def get_bool_env(var_name: str, default: bool = False) -> bool:
    """
    Safely converts an environment variable to a boolean.
    Accepts 'True', 'true', '1', 'yes' as True.
    """
    value = os.getenv(var_name, str(default))
    return value.lower() in ('true', '1', 'yes')

def get_int_env(var_name: str, default: int) -> int:
    """
    Safely converts an environment variable to an integer.
    """
    try:
        return int(os.getenv(var_name, default))
    except (ValueError, TypeError):
        print(f"Warning: Invalid integer for {var_name}, using default: {default}")
        return default

def get_list_env(var_name: str, default: list = None) -> list:
    """
    Converts a comma-separated environment variable into a list.
    Filters out empty strings.
    """
    if default is None:
        default = []
    value = os.getenv(var_name, '')
    if not value:
        return default
    return [item.strip() for item in value.split(',') if item.strip()]
