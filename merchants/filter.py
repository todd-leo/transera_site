import django_filters as filters
from django.utils.timezone import now

from .models import Merchant

class MerchantFilter(filters.FilterSet):
    def __init__(self, *a, **kw):
        print("MerchantFilter INIT")
        super().__init__(*a, **kw)

    # choices 字段直接会渲染下拉
    auth_type = filters.ChoiceFilter(choices=Merchant.AuthType.choices, label="认证类型")
    status = filters.ChoiceFilter(choices=Merchant.Status.choices, label="商户状态")
    risk_level = filters.ChoiceFilter(choices=Merchant.RiskLevel.choices, label="风险等级")
    region = filters.ChoiceFilter(choices=Merchant.Region.choices, label="注册地区")

    # 普通字符字段
    distributor = filters.CharFilter(label="所属分销/渠道", lookup_expr="icontains")
    account = filters.CharFilter(label="注册账号", lookup_expr="icontains")
    name = filters.CharFilter(label="商户名称", lookup_expr="icontains")
    id = filters.CharFilter(label="商户编号", lookup_expr="icontains")

    # 日期范围
    register_time = filters.DateFromToRangeFilter(label="注册时间")
    last_eval_time = filters.DateFromToRangeFilter(label="最近评估时间")

    # 外键（上级）
    parent = filters.ModelChoiceFilter(
        label="所属上级",
        field_name="parent",
        queryset=Merchant.objects.all()
    )

    class Meta:
        model = Merchant
        # 指定可过滤的字段集合（可只保留你需要的）
        fields = [
            "id", "name", "auth_type", "account", "status",
            "risk_level", "region", "distributor", "parent",
            "register_time", "last_eval_time",
        ]