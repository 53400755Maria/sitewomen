from django import template
from women.views import menu
from women.models import Category
from women.models import TagPost

register = template.Library()

@register.simple_tag(name='get_menu')
def get_menu():
    return menu

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}