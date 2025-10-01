from django.urls import reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import Menu, AdminOnlyMenuItem, SubmenuMenuItem

from merchants.admin.merchants import MerchantViewSet
from users.admin import UserViewSet


@hooks.register("register_admin_viewset")
def register_merchant_viewset():
    return MerchantViewSet()

@hooks.register("register_admin_viewset")
def register_user_viewset():
    return UserViewSet()

# 顶层分组：必须返回 SubmenuMenuItem（不要返回 Menu 本体）
@hooks.register("register_admin_menu_item")
def register_merchant_group():
    group_menu = Menu(register_hook_name="register_merchant_menu_item")
    return SubmenuMenuItem(
        "商户",
        group_menu,
        icon_name="group",
        order=120,
    )

@hooks.register("register_merchant_menu_item")
def register_merchant_manage_item():
    index_url = reverse(MerchantViewSet().get_url_name("index"))
    return AdminOnlyMenuItem(
        label="商户管理",
        url=index_url,
        icon_name="user",
        order=120  # 排序权重，数字越小越靠前
    )

@hooks.register("register_merchant_menu_item")
def register_user_manage_item():
    index_url = reverse(UserViewSet().get_url_name("index"))
    return AdminOnlyMenuItem(
        label="用户管理",
        url=index_url,
        icon_name="user",
        order=110
    )

@hooks.register("insert_global_admin_css")
def add_horizontal_scroll_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        "/static/merchants/admin_overflow.css"
    )