from django import template
from ..views import render_menu

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
    request = context['request']
    return render_menu(menu_name, request) 