from django import template

register = template.Library()

@register.filter
def ranged(end):
    return range(end+1)

@register.filter
def max_columns(value):
    return max(len(row) for row in value)

@register.filter
def ranger(num):
    return range(num)

