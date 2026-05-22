from openai import OpenAI
import json
import os

from utils.datetime_helper import now

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.deepseek.com/v1"
)


ALLOWED_CATEGORIES = ["工作", "学习", "生活", "娱乐", "其他"]

ALLOWED_TAGS = [
    "python",
    "AI",
    "SQL",
    "英语",
    "运动",
    "购物",
]


class AIService:
    def parse_task(self, user_input):
        prompt = f"""
你是一个任务解析器

用户输入:
{user_input}

现在的时间是:
{now()}

请提取:
1. title: 任务标题
2. priority: 任务优先级，0-5的数字，0表示最低优先级，5表示最高优先级，如果用户没有指定优先级，请默认为2
3. due_at: 任务截止时间，格式为YYYY-MM-DD HH:MM，如果时间不完整则自动补全现在的时间，如果用户没有指定截止时间，请返回空字符串

请根据输入判断:
1. category: 只能从一下选择中选择一个{ALLOWED_CATEGORIES}，如果用户没有指定或者无法判断，请返回空字符串
2. tags: 先从以有的tags中寻找关键词{ALLOWED_TAGS}，如果用户输入中包含这些关键词，则返回对应的标签，如果没有找到匹配的标签，则返回一个空列表，最多选择3个标签

返回JSON格式，示例如下:
{{
    "title": "买菜",
    "priority": 3,
    "category": "生活",
    "tags": ["购物", "家庭"],
    "due_at": "2024-06-30 18:00"
}}
"""
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {
                    "role": "system",
                    "content": "你是JSON API，只能返回纯JSON，不允许解释"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        content = response.choices[0].message.content
        return json.loads(content)


    