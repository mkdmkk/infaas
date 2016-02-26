from django import template

register = template.Library()


@register.filter('range')
def pythonic_range(right, left=0):
    return range(left, right)