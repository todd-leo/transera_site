from django.db import models

class Merchant(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待审核"
        ACTIVE = "active", "正常"
        SUSPENDED = "suspended", "已冻结"

    name = models.CharField("商户名称", max_length=200, db_index=True)
    license_no = models.CharField("营业执照号", max_length=100, blank=True)
    contact_name = models.CharField("联系人", max_length=100, blank=True)
    contact_phone = models.CharField("联系电话", max_length=50, blank=True)
    status = models.CharField("状态", max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "商户"
        verbose_name_plural = "商户"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name