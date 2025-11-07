from django import template

register = template.Library()

@register.filter
def before_at(value):
    """Returns the part of the email before @"""
    return value.split('@')[0]
