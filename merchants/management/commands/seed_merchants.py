import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from merchants.models import Merchant

FIRST_NAMES = ["华夏", "恒信", "万象", "云舟", "星河", "纵横", "启航", "新锐", "极客", "凌云"]
INDUSTRIES = ["零售", "餐饮", "教育", "出行", "医疗", "房产", "文娱", "电商", "政务", "物流"]

def rand_name():
    return random.choice(FIRST_NAMES) + random.choice(INDUSTRIES)

def rand_account():
    return f"acct{random.randint(100000, 999999)}"

def rand_phone():
    return f"1{random.randint(3000000000, 9999999999)}"

class Command(BaseCommand):
    help = "Seed test merchants"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20)

    def handle(self, *args, **options):
        count = options["count"]
        now = timezone.now()

        created = 0
        for _ in range(count):
            reg_dt = now - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
            last_eval = reg_dt + timedelta(days=random.randint(0, 300))

            m = Merchant(
                id=f"M{random.randint(100000, 999999)}",  # 你的主键是 CharField(primary_key=True)
                name=rand_name(),
                auth_type=random.choice([c[0] for c in Merchant.AuthType.choices]),
                account=rand_phone(),
                status=random.choice([c[0] for c in Merchant.Status.choices]),
                risk_level=random.choice([c[0] for c in Merchant.RiskLevel.choices]),
                region=random.choice([c[0] for c in Merchant.Region.choices]),

                register_time=reg_dt,
                last_eval_time=last_eval,
                distributor=random.choice(["直销", "代理A", "代理B", "渠道伙伴"]),
                accounts_apply_limit=random.randint(1, 50),
                accounts_applied=random.randint(0, 50),
                comments="测试数据",
            )
            # 可选：随机挂到某个已有上级
            if Merchant.objects.exists() and random.random() < 0.3:
                m.parent = random.choice(list(Merchant.objects.all()))
            try:
                m.save()
                created += 1
            except Exception as e:
                self.stderr.write(f"skip {m.id}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Created {created} merchants"))