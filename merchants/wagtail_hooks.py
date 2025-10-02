from django.urls import reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import Menu, AdminOnlyMenuItem, SubmenuMenuItem
from wagtail.admin.viewsets.model import ModelViewSetGroup

from merchants.admin.merchants import MerchantViewSet
from users.admin import UserViewSet


class MerchantGroup(ModelViewSetGroup):
    menu_label = "商户"
    icon = "group"
    menu_order = 120
    items = (UserViewSet,MerchantViewSet)

@hooks.register("register_admin_viewset")
def register_group():
    return MerchantGroup()

@hooks.register("insert_global_admin_css")
def add_horizontal_scroll_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        "/static/merchants/admin_overflow.css"
    )