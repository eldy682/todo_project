from utils import validator
from repo import task_repo as repo
from service.errors import ValidationError, NotFoundError


def normalize_title(title):
    if not isinstance(title, str):
        raise ValidationError("标题必须是字符串")

    title = title.strip()
    if not title:
        raise ValidationError("标题不能为空")

    return title


def normalize_priority(priority):
    if priority == "":
        return 2
    
    try:
        priority = int(priority)
    except ValueError:
        raise ValidationError("优先级必须是数字")
    
    if not (0 <= priority <= 5):
        raise ValidationError("优先级只能是0-5")
    
    return priority


def normalize_keyword(keyword):
    if not isinstance(keyword, str):
        raise ValidationError("关键词必须是字符串")
    
    keyword = keyword.strip()
    if not keyword:
        raise ValidationError("关键词不能为空")

    return keyword

def get_valid_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        raise ValidationError("任务ID必须是数字")
    
    task = repo.get_task_by_id(task_id)
    if not task:
        raise NotFoundError("任务不存在")
    
    return task