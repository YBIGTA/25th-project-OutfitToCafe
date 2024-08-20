from django import template

register = template.Library()

@register.filter(name='star_rating')
def star_rating(value):
    if value is None:
        return '☆☆☆☆☆'  # rating이 None일 경우 빈 별 반환
    
    try:
        value = float(value)
    except ValueError:
        return ''
    
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    return '★' * full_stars + '½' * half_star + '☆' * empty_stars
