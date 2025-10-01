# users/management/commands/seed_users.py
import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from users.models import User

# 固定用户常量
FIXED_EMAIL = "todd.f.leo@gmail.com"
FIXED_PASSWORD = "1qaz@WSX"
FIXED_PAYLOAD_STATIC = {
    # 除了时间相关项，其余字段固定
    "id": "U000000000000000000000000000001",
    "register_account": "todd_leo",
    "register_system": "高博融汇",
    "verify_code": "R_FIXED_00001",
    "distributor_id": "A000110",
    "distributor_template_id": "00000200",
    "is_active": True,
    "failed_count": 0,
    "wechat_id": "wx_todd_leo_001",
    "wechat_name": "Todd Leo",
}

# 随机生成所需的枚举
BRANCH_CODES = ["A000110", "B000195", "C000201"]
TEMPLATE_CODES = ["00000200", "00000300"]
REGISTER_SYSTEMS = ["高博融汇", "官网注册", "活动页"]
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "163.com", "qq.com", "hotmail.com", "proton.me"]


def rand_email() -> str:
    local_part = f"user{random.randint(100000, 999999)}"
    return f"{local_part}@{random.choice(EMAIL_DOMAINS)}"


def rand_id(seed_index: int) -> str:
    ts = timezone.now().strftime("%y%m%d%H%M%S")
    tail = f"{seed_index:04d}{random.randint(1000,9999)}"
    return f"U{ts}{tail}"[:32]


def rand_verify_code() -> str:
    day = timezone.now().strftime("%y%m%d")
    hex_part = "".join(random.choices("0123456789ABCDEF", k=5))
    return f"R{day}{hex_part}"


class Command(BaseCommand):
    help = "Seed users: fixed user (default), special user (--email/--password), or random users (--count)."

    def add_arguments(self, parser):
        # 模式二：特殊用户
        parser.add_argument("--email", type=str, help="Only create a special user with this email.")
        parser.add_argument("--password", type=str, help="Password for the special user.")

        # 模式三：随机用户
        parser.add_argument("--count", type=int, help="Only create N random users.")
        parser.add_argument("--days", type=int, default=30, help="(仍保留但不影响注册时间) 其他时间字段可能参考。")

        # 可选：给特殊用户覆盖部分固定字段（不影响固定用户模式）
        parser.add_argument("--distributor", type=str, help="Distributor ID for the special user (optional).")
        parser.add_argument("--template", type=str, help="Distributor template ID for the special user (optional).")

    @transaction.atomic
    def handle(self, *args, **options):
        email = options.get("email")
        password = options.get("password")
        count = options.get("count")

        # 互斥校验
        if (email or password) and (count is not None):
            raise CommandError("参数冲突：--email/--password 与 --count 不能同时使用。")

        if email or password:
            if not email or not password:
                raise CommandError("特殊用户模式需要同时提供 --email 与 --password。")
            distributor = options.get("distributor")
            template = options.get("template")
            created, updated = self.upsert_special_user(email, password, distributor, template)
            self.stdout.write(self.style.SUCCESS(f"special user done. created={created}, updated={updated}"))
            return

        if count is not None:
            if count <= 0:
                raise CommandError("--count 必须为正整数。")
            created = self.create_random_users(count=count)
            self.stdout.write(self.style.SUCCESS(f"random users done. created={created}"))
            return

        # 模式一：仅创建固定用户
        created, updated = self.upsert_fixed_user()
        self.stdout.write(self.style.SUCCESS(f"fixed user done. created={created}, updated={updated}"))

    # ----------------- 具体实现 -----------------

    def upsert_fixed_user(self) -> tuple[int, int]:
        """
        注册时间、register_date、last_login 统一为当前时间（last_login 可为 None，如需固定为当前就设为 now）。
        若用户已存在则不修改，保持之前固定值；不存在则以当前时间创建。
        """
        now = timezone.now()
        qs = User.objects.filter(register_email=FIXED_EMAIL)
        payload = {
            **FIXED_PAYLOAD_STATIC,
            "register_email": FIXED_EMAIL,
            "password": make_password(FIXED_PASSWORD),
            "register_time": now,
            "register_date": now,
            "last_login": None
        }

        if qs.exists():
            # 不覆盖，保持既有固定字段
            return 0, 0
        User.objects.create(**payload)
        return 1, 0

    def upsert_special_user(
        self, email: str, password: str, distributor: str | None, template: str | None
    ) -> tuple[int, int]:
        """
        特殊用户：所有字段固定，且每次执行都会覆盖为固定值；
        时间字段统一写入当前系统时间。
        """
        now = timezone.now()
        payload = {
            "id": "U_SPECIAL_" + (email.replace("@", "_").replace(".", "_"))[:20],
            "register_account": email.split("@")[0],
            "register_email": email,
            "register_system": "脚本创建",
            "register_time": now,
            "verify_code": "R_SPECIAL_" + now.strftime("%y%m%d"),
            "distributor_id": distributor or "A000110",
            "distributor_template_id": template or "00000200",
            "password": make_password(password),
            "is_active": True,
            "failed_count": 0,
            "wechat_id": None,
            "wechat_name": None,
            "register_date": now,
            "last_login": None
        }

        obj, created = User.objects.update_or_create(
            register_email=email, defaults=payload
        )
        return (1, 0) if created else (0, 1)

    def create_random_users(self, count: int) -> int:
        """
        随机用户：注册时间、register_date、last_login 全部设为当前系统时间。
        """
        now = timezone.now()
        created = 0
        for i in range(1, count + 1):
            reg_email = rand_email()
            defaults = {
                "id": rand_id(i),
                "register_account": str(random.randint(13000000000, 19999999999)),
                "register_email": reg_email,
                "register_system": random.choice(REGISTER_SYSTEMS),
                "register_time": now,
                "verify_code": rand_verify_code(),
                "distributor_id": random.choice(BRANCH_CODES),
                "distributor_template_id": random.choice(TEMPLATE_CODES),
                "password": make_password("Passw0rd!"),
                "is_active": random.choice([True, True, True, False]),
                "failed_count": random.randint(0, 3),
                "wechat_id": random.choice([None, "wx_1001", "wx_1002", "wx_1003"]),
                "wechat_name": random.choice([None, "小王", "阿强", "小李"]),
                "register_date": now,
                "last_login": now,  # 如需 None 可改
            }

            obj, created_flag = User.objects.get_or_create(
                register_email=reg_email, defaults=defaults
            )
            if created_flag:
                created += 1
        return created