from wagtail.admin.viewsets.model import ModelViewSet

from users.models import User as AppUser


class UserViewSet(ModelViewSet):
    model = AppUser
    icon = "user"
    menu_label = "用户管理"
    name = "users"           # 用于 URL 前缀/命名空间
    add_to_admin_menu = False  # 由分组来统一加到菜单
    list_display = [
        "id", "register_account", "register_email", "distributor_id",
        "is_active", "last_login", "register_time",
    ]
    list_filter = ["is_active", "distributor_id"]
    search_fields = ["register_email", "register_account", "wechat_name", "wechat_id"]
    ordering = ["-register_time"]
    exclude_form_fields = []