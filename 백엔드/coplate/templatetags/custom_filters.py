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
    
    rounded_value = int(value)  # 소수점 이하 반올림 없이 정수 부분만 사용
    if value >= 4.0 and value < 5.0:
        rounded_value = 4
    
    empty_stars = 5 - rounded_value

    return '★' * rounded_value + '☆' * empty_stars
