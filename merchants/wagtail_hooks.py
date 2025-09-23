from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import Menu, AdminOnlyMenuItem, SubmenuMenuItem
from wagtail.admin.viewsets.model import ModelViewSet

from .models import Merchant

class MerchantViewSet(ModelViewSet):
    model = Merchant
    icon = "user"
    add_to_admin_menu = False

    list_display = [
        "name",
        "id",
        "account",
        "region",
        "auth_type",
        "risk_level",
        "last_eval_time",
        "status",
        "channel",
        "can_apply_accounts",
        "applied_accounts",
        "utilization_rate",
    ]

    list_filter = [
        "auth_type",
        "status",
        "risk_level",
        "channel",
        ("register_time", {"label": "注册时间"}),  # 日期范围过滤
        "region",
        ("parent", {"label": "所属上级"}),
    ]

    search_fields = ["name", "merchant_code", "account", "region", "parent__name", "parent__merchant_code"]

    ordering = ["-register_time"]

# class MerchantViewSet(ModelViewSet):
#     prefix = "merchant"
#     model = Merchant
#     icon = "user"
#     add_to_admin_menu = False
#
#     list_display = ["name", "license_no", "contact_name", "contact_phone", "status", "created_at"]
#     list_filter = ["status", "created_at"]
#     search_fields = ["name", "license_no", "contact_name", "contact_phone"]
#     ordering = ["-created_at"]
#
#     # 如果模型没有 panels/edit_handler，必须声明表单字段
#     form_fields = ["name", "license_no", "contact_name", "contact_phone", "status"]

@hooks.register("register_admin_viewset")
def register_merchant_viewset():
    return MerchantViewSet()

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
    # index_url = reverse(MerchantViewSet.get_url_name("index"))
    index_url = reverse(f"{MerchantViewSet.prefix}:index")
    return AdminOnlyMenuItem(
        label="商户管理",
        url=index_url,
        icon_name="user",
        order=120,  # 排序权重，数字越小越靠前
    )