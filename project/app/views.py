from django.shortcuts import render
from typing import List, Dict, Any, Optional
from .models import MenuItem, Menu
from django.template.loader import get_template
from django.utils.safestring import mark_safe


def build_menu_tree(menu_items: List[MenuItem], current_url: str, parent: Optional[MenuItem] = None) -> List[Dict[str, Any]]:
    """
    Строит дерево меню из списка пунктов меню.
    
    Args:
        menu_items: Список всех пунктов меню
        current_url: Текущий URL для определения активного пункта
        parent: Родительский пункт меню (None для корневых элементов)
    
    Returns:
        Список словарей с пунктами меню и их дочерними элементами
    """
    tree = []
    items = [item for item in menu_items if item.parent == parent]
    
    for item in items:
        children = build_menu_tree(menu_items, current_url, item)
        is_active = item.url == current_url or any(child.get('is_active', False) for child in children)
        
        node = {
            "item": item,
            "children": children,
            "is_active": is_active
        }
        tree.append(node)
    return tree


def render_menu(menu_name: str, request) -> str:
    """
    Рендерит меню по его названию.
    
    Args:
        menu_name: Название меню для отображения
        request: HTTP запрос для получения текущего URL
    
    Returns:
        HTML-код отрендеренного меню
    """
    try:
        # Находим меню по названию с предзагрузкой всех пунктов
        menu = Menu.objects.prefetch_related(
            'items__parent',
            'items__menu'
        ).get(name=menu_name)
        
        # Получаем текущий URL
        current_url = request.path
        
        # Получаем все пункты этого меню (уже загружены через prefetch_related)
        # noinspection PyUnresolvedReferences
        all_items = list(menu.items.all())
        
        # Строим дерево меню с учетом текущего URL
        menu_tree = build_menu_tree(all_items, current_url)
        
        # Рендерим шаблон
        template = get_template('app/draw_menu.html')
        html = template.render({
            'menu': menu,
            'menu_tree': menu_tree,
            'current_path': current_url
        })
        
        return mark_safe(html)
        
    except Menu.DoesNotExist:
        return ''


def menu_demo(request):
    """
    Отображает демо-страницу с меню.
    Оптимизировано: используется prefetch_related для загрузки всех данных одним запросом.
    """
    try:
        # Получаем все меню с предзагрузкой всех пунктов одним запросом
        menus = Menu.objects.prefetch_related(
            'items__parent',
            'items__menu'
        ).all()
        
        menu_data = []
        
        # Для каждого меню строим дерево (данные уже загружены)
        for menu in menus:
            # Получаем все пункты этого меню (уже загружены через prefetch_related)
            # noinspection PyUnresolvedReferences
            all_items = list(menu.items.all())
            menu_tree = build_menu_tree(all_items, request.path)
            menu_data.append({
                'menu': menu,
                'menu_tree': menu_tree
            })
        
        return render(request, "app/menu_demo.html", {
            "menu_data": menu_data,
            "request": request,
        })
        
    except Exception as e:
        return render(request, "app/menu_demo.html", {
            "menu_data": [],
            "request": request,
        })

