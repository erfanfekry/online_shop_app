from django import template

register = template.Library()

@register.filter
def intcomma(value):
    try:
        return f'{int(value):,}'
    except:
        return value
