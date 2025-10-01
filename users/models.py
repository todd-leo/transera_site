from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    id = models.CharField(
        "用户ID", max_length=32, primary_key=True
    )

    # 注册信息
    register_account = models.CharField(
        "注册账号", max_length=64, blank=True, null=True, db_index=True
    )
    register_email = models.EmailField(
        "注册邮箱", blank=True, null=True, db_index=True
    )
    register_system = models.CharField(
        "注册系统", max_length=32, blank=True, null=True
    )
    register_time = models.DateTimeField(
        "注册时间", blank=True, null=True, db_index=True
    )

    # 认证与渠道
    verify_code = models.CharField(
        "认证编码", max_length=32, blank=True, null=True, db_index=True
    )
    distributor_id = models.CharField(
        "分销编码", max_length=16, blank=True, null=True, db_index=True
    )
    distributor_template_id = models.CharField(
        "分销模板编码", max_length=16, blank=True, null=True
    )

    # 登录与状态
    password = models.CharField("密码哈希", max_length=128, blank=True, null=True)
    is_active = models.BooleanField("用户状态", default=True)
    failed_count = models.PositiveIntegerField("登陆失败次数", default=0)
    wechat_id = models.CharField("微信ID", max_length=64, blank=True, null=True)
    wechat_name = models.CharField("微信名称", max_length=64, blank=True, null=True)

    # 审计
    register_date = models.DateTimeField("创建时间", auto_now_add=True)
    last_login = models.DateTimeField("最后登录时间", blank=True, null=True)

    class Meta:
        db_table = "users"
        verbose_name = "前台用户"
        verbose_name_plural = "前台用户"
        indexes = [
            models.Index(fields=["register_email"]),
            models.Index(fields=["register_account"]),
            models.Index(fields=["register_time"]),
            models.Index(fields=["distributor_id"]),
        ]

    def __str__(self):
        return f"{self.id} / {self.register_email or self.register_account or ''}".strip()

    def set_password(self, raw_password: str):
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        if not self.password:
            return False
        return check_password(raw_password, self.password)