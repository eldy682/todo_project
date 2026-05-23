import pytest

from app.errors import errors
from app.service import service_helper


ALLOWED_CATEGORIES = ["工作", "学习", "生活", "娱乐", "其他"]

ALLOWED_TAGS = [
    "python",
    "AI",
    "SQL",
    "英语",
    "运动",
    "购物",
]


def test_normalize_title():
    assert service_helper.normalize_title("  Task  ") == "Task"
    with pytest.raises(errors.ValidationError, match="标题不能为空"):
        service_helper.normalize_title(" ")
    with pytest.raises(errors.ValidationError, match="标题必须是字符串"):
        service_helper.normalize_title(123)


def test_normalize_priority():
    assert service_helper.normalize_priority("") == 2
    assert service_helper.normalize_priority("3") == 3
    with pytest.raises(errors.ValidationError, match="优先级必须是数字"):
        service_helper.normalize_priority("abc")
    with pytest.raises(errors.ValidationError, match="优先级只能是0-5"):
        service_helper.normalize_priority("-1")
    with pytest.raises(errors.ValidationError, match="优先级只能是0-5"):
        service_helper.normalize_priority("6")


def test_normalize_keyword():
    assert service_helper.normalize_keyword("  keyword  ") == "keyword"
    with pytest.raises(errors.ValidationError, match="关键词不能为空"):
        service_helper.normalize_keyword(" ")
    with pytest.raises(errors.ValidationError, match="关键词必须是字符串"):
        service_helper.normalize_keyword(123)


def test_get_valid_task():
    with pytest.raises(errors.ValidationError, match="任务ID必须是数字"):
        service_helper.get_valid_task("abc")
    with pytest.raises(errors.NotFoundError, match="任务不存在"):
        service_helper.get_valid_task("9999")


def test_normalize_category():
    assert service_helper.normalize_category(" 工作 ") == "工作"
    with pytest.raises(errors.ValidationError, match="种类不能为空"):
        service_helper.normalize_category(" ")
    with pytest.raises(errors.ValidationError, match="种类必须是字符串"):
        service_helper.normalize_category(123)
    with pytest.raises(errors.ValidationError, match="种类不存在"):
        service_helper.normalize_category("未知")


def test_normalize_tags():
    assert service_helper.normalize_tags(" python ") == "python"
    with pytest.raises(errors.ValidationError, match="标签不能为空"):
        service_helper.normalize_tags(" ")
    with pytest.raises(errors.ValidationError, match="标签必须是字符串"):
        service_helper.normalize_tags(123)
    with pytest.raises(errors.ValidationError, match="标签不存在"):
        service_helper.normalize_tags("未知")