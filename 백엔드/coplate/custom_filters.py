from django import template

register = template.Library()

@register.filter
def star_rating(value):
    full_stars = int(value)
    half_star = value - full_stars
    stars = '★' * full_stars
    if half_star >= 0.5:
        stars += '★'
    return stars.ljust(5, '☆')
