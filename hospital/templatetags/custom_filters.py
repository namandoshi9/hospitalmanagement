from django import template

register = template.Library()

@register.filter(name='hide_digits_before_second_dash')
def hide_digits_before_second_dash(value):
    parts = value.split('-')
    if len(parts) >= 3:
        return parts[0] + '-' + '-'.join(parts[2:])
    return value


