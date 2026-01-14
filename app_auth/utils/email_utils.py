def get_email_local_part(value: str) -> str:
    if not isinstance(value, str) or '@' not in value:
        return value
    return value.split('@', 1)[0].strip()