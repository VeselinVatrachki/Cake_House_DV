from django import template

register = template.Library()


@register.filter
def stars(rating):
    """Render a numeric 1–5 rating as star characters."""
    try:
        n = int(rating)
    except (TypeError, ValueError):
        return ''
    n = max(0, min(5, n))
    return '★' * n + '☆' * (5 - n)


@register.simple_tag
def page_title(site_name, page=''):
    if page:
        return f'{page} · {site_name}'
    return site_name
