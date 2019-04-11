from django.utils.html import format_html
from .models import MenuInfo

menu_active = ''


def make_menus(menus,root=False,menu_id=None,active=None):
    make_html = ''
    for menu in menus:
        child_menu_flag = "treeview"
        menu_right_flag = '<span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span>'
        # child_menu = '<li class="{active}"><a href="{menu_url}"><i class="fa fa-circle-o"></i> {menu_name}</a></li>'
        child_menu = '<li class="{active}"><a href="javascript:;" menu_url="{menu_url}" onclick="link(this)"><i class="fa fa-circle-o"></i> {menu_name}</a></li>'
        child_menu_html = '<ul class="treeview-menu">{make_child_menu_html}</ul>'
        master_menu_html = """
                <li class="{child_menu_flag} {active}">
                    <a href="{menu_url}"><i class="fa {menu_icon}"></i> <span>{menu_name}</span>{menu_right_flag}</a>
                    <ul class="treeview-menu">
                    {children_menu_html}
                    </ul>
                </li>"""
        children_menu_html = """
                <li class="treeview">
                    <a href="{menu_url}"><i class="fa {menu_icon}"></i> <span>{menu_name}</span>{menu_right_flag}</a>
                    {child_menu_html}
                </li>"""
        parent = menu.parent
        active_menu = ''
        menu_icon = menu.menu_icon.ClassName

        if root and parent:
            continue

        if root and not parent:
            make_children_menu_html = make_menus(menus, root=False, menu_id=menu.id, active=active)
            make_master_menu_html = master_menu_html.format(child_menu_flag=child_menu_flag,
                                                            active=active_menu,
                                                            menu_url=menu.url,
                                                            menu_icon=menu_icon,
                                                            menu_name=menu.name,
                                                            menu_right_flag=menu_right_flag,
                                                            children_menu_html=make_children_menu_html)
            make_html += make_master_menu_html
        elif parent and parent.id == menu_id:
            make_child_menu_html = make_menus(menus, root=False, menu_id=menu.id, active=active)
            menu_icon = menu.menu_icon.ClassName
            if make_child_menu_html:
                child_menu_html = child_menu_html.format(make_child_menu_html=make_child_menu_html)
                children_menu_html = children_menu_html.format(menu_url=menu.url,
                                                               menu_icon=menu_icon,
                                                               menu_name=menu.name,
                                                               menu_right_flag=menu_right_flag,
                                                               child_menu_html=child_menu_html)
            else:
                children_menu_html = child_menu.format(menu_url=menu.url, menu_name=menu.name, active=active_menu)
            make_html += children_menu_html
        else:
            continue
    return make_html

def make_menus_html(menus, parent_id=None, current_parent_id=None, active=None):
    """
    menus = Menus.objects.all()
    :param menus: 寻找的对象，传一个queryset对象
    :param parent_id: 父级菜单ID
    :param current_parent_id: 当前父级菜单ID
    :param active: 激活的菜单名
    :return:
    """
    make_html = ""
    for menu in menus:
        child_menu_flag = "treeview"
        menu_right_flag = '<span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i></span>'
        child_menu = '<li class="{active}"><a href="{menu_url}"><i class="fa fa-circle-o"></i> {menu_name}</a></li>'
        child_menu_html = '<ul class="treeview-menu">{make_child_menu_html}</ul>'
        master_menu_html = """
        <li class="{child_menu_flag} {active}">
            <a href="{menu_url}"><i class="fa {menu_icon}"></i> <span>{menu_name}</span>{menu_right_flag}</a>
            <ul class="treeview-menu">
            {children_menu_html}
            </ul>
        </li>"""
        children_menu_html = """
        <li class="treeview {active}">
            <a href="{menu_url}"><i class="fa {menu_icon}"></i> <span>{menu_name}</span>{menu_right_flag}</a>
            {child_menu_html}
        </li>"""
        parent = menu.parent  # 获取当前菜单的父级菜单
        active_menu = ''
        if current_parent_id == menu.id or (not parent and current_parent_id):
            continue  # 如果当前父级菜单ID是自己或没有父级菜单且有当前父级ID则跳过本次循环
        if not parent and current_parent_id is None:  # 如果没有父级菜单且当前父级ID是None
            make_children_menu_html = make_menus_html(menus, parent_id=parent_id, current_parent_id=menu.id)
            if not make_children_menu_html:
                menu_right_flag = ''
            menu_icon = menu.menu_icon.ClassName
            if hasattr(menu, 'icon_name'):
                menu_icon = menu.icon_name
            active = menu_active.split('/')[1]
            active = '/%s/' % active
            if menu.url == active:
                active_menu = 'active'
            else:
                active_menu = ''
            make_master_menu_html = master_menu_html.format(child_menu_flag=child_menu_flag,
                                                            active=active_menu,
                                                            menu_url=menu.url,
                                                            menu_icon=menu_icon,
                                                            menu_name=menu.name,
                                                            menu_right_flag=menu_right_flag,
                                                            children_menu_html=make_children_menu_html)
            make_html += make_master_menu_html
        elif parent and current_parent_id == parent.id:  # 如果有父级且当前父级ID是自己的父级ID4
            make_child_menu_html = make_menus_html(menus, parent_id=current_parent_id, current_parent_id=menu.id,active=menu_active)
            menu_icon = menu.menu_icon.ClassName


            if menu.url == menu_active:
                active_menu = 'active'
            else:
                active_menu = ''
            if make_child_menu_html:
                child_menu_html = child_menu_html.format(make_child_menu_html=make_child_menu_html)
                children_menu_html = children_menu_html.format(active=active_menu,
                                                               menu_url=menu.url,
                                                               menu_icon=menu_icon,
                                                               menu_name=menu.name,
                                                               menu_right_flag=menu_right_flag,
                                                               child_menu_html=child_menu_html)
            else:
                children_menu_html = child_menu.format(menu_url=menu.url, menu_name=menu.name, active=active_menu)
            make_html += children_menu_html
        else:
            continue
    return make_html


def make_menus_processor(request):
    menus_obj = MenuInfo.objects.filter(show=1).order_by('parent', 'priority')
    # global menu_active
    # menu_active = request.path
    # menus = make_menus_html(menus=menus_obj, active=menu_active)
    menus = make_menus(menus_obj,root=True)
    return {'menus': format_html(menus)}
