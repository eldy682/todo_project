import json
from app.db.base import execute_query
from app.repo.task_repo import TaskRepo
from app.errors.errors import ValidationError, NotFoundError

task_repo = TaskRepo(execute_query)

ALLOWED_CATEGORIES = ["工作", "学习", "生活", "娱乐", "其他"]

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
    
    task = task_repo.get_task_by_id(task_id)
    if not task:
        raise NotFoundError("任务不存在")
    
    return task

def normalize_category(category):
    if not isinstance(category, str):
        raise ValidationError("种类必须是字符串")
    
    category = category.strip().lower()
    if not category:
        raise ValidationError("种类不能为空")
    
    if category not in ALLOWED_CATEGORIES:
        raise ValidationError("种类不存在")

    return category

def normalize_tag(tag):
    if not isinstance(tag, str):
        raise ValidationError("标签必须是字符串")
    
    tag = tag.strip().lower()
    if not tag:
        raise ValidationError("标签不能为空")

    return tag

def normalize_tags(tags):
    if not isinstance(tags, (str, list)):
        raise ValidationError("标签必须是字符串或字符串列表")
    
    if isinstance(tags, str):   
        tags = [tag.strip() for tag in tags.split(" ") if tag.strip()]
    
    return [normalize_tag(tag) for tag in tags]