from datetime import datetime


def validate_title(title):
    return bool(title.strip())


def validate_datetime(dt_str):
    try:
        datetime.strptime(dt_str.strip(), "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
 

def validate_keyword(keyword):
    return bool(keyword.strip())
