import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# 사용자 정의 필터 정의
# {{ xxx|mark }}
@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

# 사용자 정의 태그 정의
# {% avatar user.id %}
@register.simple_tag()
def avatar(uid):
    tag = f'<img class="avatar" src="https://randomuser.me/api/portraits/men/{uid}.jpg"/>'
    return mark_safe(tag)

