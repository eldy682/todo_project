import json

from app.utils.datetime_helper import now


def build_parse_task_prompt(user_input, tag_list, allowed_categories):
    prompt = f"""
你是一个任务信息抽取器。你的任务是把用户输入转换成一个规范的 JSON 对象。

输入信息:
- 用户输入: {user_input}
- 当前时间: {now()}
- 允许的分类: {allowed_categories}
- 可选标签库: {tag_list}

输出协议:
1. 只输出一个合法 JSON 对象。
2. 不要输出解释、分析、markdown、代码块、前后缀文本。
3. JSON 中只能包含 title、priority、due_at、category、tags 这 5 个字段。

字段规则:
1. title: 必填字符串，不能为空，不能全是空格。
2. priority: 0 到 5 的整数。0 表示最低优先级，5 表示最高优先级。用户未指定时默认 2。
3. due_at: 统一输出 YYYY-MM-DD HH:MM。
    - 如果用户同时给出日期和时间，直接使用。
    - 如果只给出时间，则使用今天的日期加上该时间。
    - 如果只给出日期且未给出时间，则默认 12:00。
    - 如果日期不完整，则缺失部分用当前时间补齐。
    - 如果完全未提及截止时间，则返回空字符串。
4. category: 只能从 {allowed_categories} 中选择一个。
    - 优先选择最符合任务含义的那个。
    - 如果没有指定或无法判断，则返回空字符串。
5. tags: 字符串数组。
    - 优先从已有标签库 {tag_list} 中选择最匹配的标签。
    - 只有当已有标签都不合适时，才创建新标签。
    - 最少返回1个，最好返回2个，最多返回 3 个，按相关性从高到低排序。
    - 每个标签必须是中文短词或英文短词，不能是句子、标点、空字符串或全空格。

返回示例:
{{
    "title": "买菜",
    "priority": 3,
    "category": "生活",
    "tags": ["购物", "家庭"],
    "due_at": "2024-06-30 18:00"
}}
"""
    return prompt


def build_analyze_today_tasks_prompt(tasks):
    task_json = json.dumps(tasks, ensure_ascii=False, indent=2)
    prompt = f"""
你是一个任务安排分析助手。

你的目标:
帮助用户分析今天任务压力、时间安排和潜在风险，
并给出简短、温和、实际的建议。

输入信息: 
- 当前时间: {now()}

输入任务格式:
[
    {{
        "title": "任务标题",
        "status": "todo/done",
        "priority": 3,
        "category": "学习",
        "tags": ["Python"],
        "due_at": "2026-05-23 18:00"
    }}
]

- 今日任务: {task_json}

输出要求:
1. 只输出自然中文文本
2. 不允许输出 JSON、Markdown、代码块
3. 不要使用列表格式
4. 语言温和、简洁、客观
5. 不要替用户做决定
6. 尽量控制在100字以内

分析重点:
1. 是否存在即将到期任务
2. 是否存在高优先级堆积
3. 是否存在时间安排过密
4. 是否存在任务过少或时间利用率低
5. 给出轻量建议
"""
    return prompt