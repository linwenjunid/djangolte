from xadmin import views
from .models import MenuInfo,IconInfo, User
from xadmin.plugins.auth import UserAdmin
import xadmin


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = '数据中心'
    site_footer = '关于数据'


@xadmin.sites.register(MenuInfo)
class MenuInfoAdmin:
    list_display = ("name", 'parent', "url", 'menu_icon', "show", "priority")
    list_editable = ('url',)


@xadmin.sites.register(IconInfo)
class IconInfoAdmin:
    list_display = ("DisplayName", "ClassName", "SourceType", "CreateTime")


class UserInfoAdmin(UserAdmin):
    # 检索字段
    list_display = ('username', 'phone_number', 'email', 'name', 'is_staff')
    list_display_links = ('show_photo', 'username',)


xadmin.site.unregister(User)
xadmin.site.register(User, UserInfoAdmin)
