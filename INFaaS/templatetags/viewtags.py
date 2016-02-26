from django import template

register = template.Library()


@register.filter('text_overflow')
def text_overflow(text, max):
    if len(text) > max:
        return text[:max]+'...'
    else:
        return text