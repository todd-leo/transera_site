from wagtail.admin.viewsets.model import ModelViewSet

from merchants.models import Merchant


class MerchantViewSet(ModelViewSet):
    model = Merchant
    icon = "home"
    menu_label = "商户管理"
    add_to_admin_menu = False

    list_display = [
        "id",
        "name",
        "auth_type_display",
        "account",
        "region_display",
        "status_display",
        "risk_level_display",
        "parent",
        "register_time_display",
        "last_eval_time_display",
        "distributor",
        "accounts_apply_limit",
        "accounts_applied",
        "utilization_rate",
        "comments"
    ]

    list_filter = [
        "auth_type",
        "status",
        "risk_level",
        "distributor",
        # ("register_time", {"label": "注册时间"}),  # 日期范围过滤
        "region"
        # ("parent", {"label": "所属上级"}),
    ]

    search_fields = ["name", "id", "account", "region", "parent__name", "parent__merchant_code"]

    ordering = ["-register_time"]

    exclude_form_fields = []