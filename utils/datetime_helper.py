from datetime import datetime


def normalize_datetime(dt_str):
    dt_str = dt_str.strip()
    if not dt_str:
        return None
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("时间格式错误")

    return dt.strftime("%Y-%m-%d %H:%M")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")