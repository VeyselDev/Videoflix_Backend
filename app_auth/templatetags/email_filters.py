from django import template

register = template.Library()

@register.filter
def before_at(value):
    """
    Returns the part of the email before '@'.
    Returns the input unchanged if invalid.
    """
    if not isinstance(value, str) or '@' not in value:
        return value
    return value.split('@', 1)[0].strip()
