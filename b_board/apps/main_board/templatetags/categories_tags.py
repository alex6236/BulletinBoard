from django import template
from apps.main_board.models import Category

register = template.Library()


@register.inclusion_tag('main_board/categories.html')
def all_categories():
    cats = Category.objects.all()
    return {"cats": cats}

