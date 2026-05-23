from openai import OpenAI
import json
import os

from app.ai.prompts.task_prompt import build_parse_task_prompt
from app.ai.prompts.task_prompt import build_analyze_today_tasks_prompt
from app.repo.tag_repo import TagRepo

client = OpenAI(
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_BASE_URL")
)


ALLOWED_CATEGORIES = ["工作", "学习", "生活", "娱乐", "其他"]

class AIService:
    def __init__(self, tag_repo: TagRepo):
        self.tag_repo = tag_repo

    
    def get_tag_list(self):
        tags = self.tag_repo.get_all_tags()
        return [tag.name for tag in tags]


    def parse_task(self, user_input):
        tag_list = self.get_tag_list()

        prompt = build_parse_task_prompt(user_input, tag_list, ALLOWED_CATEGORIES)
        
        response = client.chat.completions.create(
            model=os.getenv("AI_MODEL"),
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "你是JSON API，只能返回一个合法JSON对象，不允许输出解释、markdown或多余文本"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        content = response.choices[0].message.content
        return json.loads(content)
    

    def analyze_today_tasks(self, tasks):
        prompt = build_analyze_today_tasks_prompt(tasks)

        response = client.chat.completions.create(
            model=os.getenv("AI_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": "你是一个任务分析器，只能输出中文文本内容，不能输出任何形式、JSON、Markdown、代码块内容，语言必须温柔平缓，不能存在过激发言，不能情绪化，只能给出建议不能擅自帮用户决定"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        content = response.choices[0].message.content
        return content
        


