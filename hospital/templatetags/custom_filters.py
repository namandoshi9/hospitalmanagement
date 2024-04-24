from django import template

register = template.Library()

@register.filter(name='remove_digits_after_second_dash')
def remove_digits_after_second_dash(value):
    parts = value.split('-')
    if len(parts) >= 3:
        parts[2] = ''.join(filter(str.isdigit, parts[2]))
        return '-'.join(parts[:2])
    return value




