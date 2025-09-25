from django.utils import timezone

WEEKDAY_ZH = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']

def fmt_dt(dt):
    """
    将 datetime -> 'YYYY-MM-dd HH:mm:ss 星期几'
    - 处理 None
    - 遵循 Django 时区设置（USE_TZ=True 时转本地）
    """
    if not dt:
        return ''
    dt = timezone.localtime(dt) # 若 USE_TZ=False，不会有副作用
    return f"{dt.strftime('%Y-%m-%d %H:%M:%S')} {WEEKDAY_ZH[dt.weekday()]}"