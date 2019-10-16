from django import template

register = template.Library()
@register.filter(name = "str2list")
def str2list(value):
    """Removes all values of arg from the given string"""
    return list(value)