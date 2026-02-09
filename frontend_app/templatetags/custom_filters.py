from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get a value from a dictionary by key"""
    if dictionary and key in dictionary:
        return dictionary.get(key, 0)
    return 0

@register.filter
def get_dict_item(dictionary, key):
    """Alternative name for the same filter"""
    return dictionary.get(key, 0) if dictionary else 0