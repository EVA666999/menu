from django import template
from django.template.loader import render_to_string
from ..models import Menu
from ..views import build_menu_tree

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """
    Тег для отображения меню по его названию.
    Использование: {% draw_menu 'menu_name' %}
    
    Args:
        context: Контекст шаблона
        menu_name: Название меню для отображения
    
    Returns:
        HTML-код отрендеренного меню
    """
    try:
        menu = Menu.objects.get(name=menu_name)
        items = list(menu.items.all())
        menu_tree = build_menu_tree(items, context['request'].path)
        return render_to_string('app/draw_menu.html', {
            'menu': menu,
            'menu_tree': menu_tree,
            'request': context['request']
        })
    except Menu.DoesNotExist:
        return '' 