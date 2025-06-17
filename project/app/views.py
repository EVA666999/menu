from django.shortcuts import render
from .models import MenuItem, Menu

def menu_demo(request):
    menus = Menu.objects.all()
    menu_data = []
    
    for menu in menus:
        items = list(menu.items.all())
        menu_tree = build_menu_tree(items, request.path)
        menu_data.append({"menu": menu, "menu_tree": menu_tree})
    
    return render(request, "app/menu_demo.html", {"menu_data": menu_data, "request": request})

def build_menu_tree(items, current_url, parent=None):
    tree = []
    for item in sorted([i for i in items if i.parent == parent], key=lambda x: x.name):
        children = build_menu_tree(items, current_url, item)
        tree.append({
            "item": item,
            "children": children,
            "is_active": item.url == current_url or any(c['is_active'] for c in children)
        })
    return tree
