from django.db import models


class Merchant(models.Model):

    # 商户认证类型
    class AuthType(models.TextChoices):
        NONE = "none", "未认证"
        PERSONAL = "personal", "个人认证"
        ENTERPRISE = "enterprise", "企业认证"

    @property
    def auth_type_display(self):
        return self.get_auth_type_display()
    auth_type_display.fget.short_description = "认证类型"

    # 商户状态
    class Status(models.TextChoices):
        ENABLED = "enabled", "活动"
        DISABLED = "disabled", "冻结"
        DELETED = "deleted", "注销"
        INACTIVE = "INACTIVE", "休眠"

    @property
    def status_display(self):
        return self.get_status_display()
    status_display.fget.short_description = "商户状态"

    class RiskLevel(models.TextChoices):
        LOW = "low", "低风险"
        MEDIUM = "medium", "中风险"
        HIGH = "high", "高风险"
        NA = "na", "暂无评估"

    @property
    def risk_level_display(self):
        return self.get_risk_level_display()
    risk_level_display.fget.short_description = "风险等级"

    class Region(models.TextChoices):
        CN = "cn", "中国大陆"
        HK = "hk", "中国香港"

    @property
    def region_display(self):
        return self.get_region_display()
    region_display.fget.short_description = "注册地区"

    id = models.CharField("商户编号", max_length=32, primary_key=True, unique=True, db_index=True)
    name = models.CharField("商户名称", max_length=255, db_index=True)
    auth_type = models.CharField("认证类型", max_length=16, choices=AuthType.choices, default=AuthType.NONE)
    account = models.CharField("注册账号", max_length=128, help_text="邮箱或手机号")
    status = models.CharField("商户状态", max_length=16, choices=Status.choices, default=Status.DISABLED)
    risk_level = models.CharField("风险等级", max_length=16, choices=RiskLevel.choices, default=RiskLevel.NA)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children", verbose_name="所属上级")
    region = models.CharField("注册地区", max_length=64, choices=Region.choices)
    register_time = models.DateTimeField("注册时间", auto_now_add=True, db_index=True)
    last_eval_time = models.DateTimeField("最近评估时间", null=True, blank=True)
    distributor = models.CharField("所属分销/渠道", max_length=64, blank=True)

    accounts_apply_limit = models.PositiveIntegerField("可申请账号数", default=0)
    accounts_applied = models.PositiveIntegerField("已申请账号数", default=0)

    comments = models.TextField("备注", blank=True)

    class Meta:
        verbose_name = "商户"
        verbose_name_plural = "商户"
        ordering = ["-register_time"]

    def __str__(self):
        return f"{self.name}({self.id})"

    @property
    def parent_name(self):
        return self.parent.name if self.parent else ""

    @property
    def parent_code(self):
        return self.parent.id if self.parent else ""

    @property
    def utilization_rate(self):
        if self.accounts_apply_limit == 0:
            return 0.0
        return round(self.accounts_applied / self.accounts_apply_limit, 4)