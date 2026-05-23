import os
from datetime import datetime
from wcwidth import wcswidth
from app.errors.errors import AppError
from app.service import service_helper
from app.service.task_service import TaskService
from app.utils.logger import logger
from app.utils.datetime_helper import now


class AppMenus:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    WHITE = "\033[97m"

    def __init__(self, task_service: TaskService):
        self.task_service = task_service
        self._menu_width = 72

    
    def _clear_screen(self):
        os.system("cls")


    def _paint(self, text, color=""):
        if not color:
            return text
        return f"{color}{text}{self.RESET}"


    def _box_line(self, left="", right=""):
        width = self._menu_width
        content_width = width - 4
        left = str(left)
        right = str(right)
        left_width = wcswidth(left)
        right_width = wcswidth(right)
        middle = max(content_width - left_width - right_width, 0)
        return f"│ {left}{' ' * middle}{right} │"


    def _render_section_title(self, title, color=None):
        marker = self._paint(f"▶ {title}", color or self.CYAN)
        print(marker)


    def _format_remaining(self, due_at):
        try:
            due_time = datetime.strptime(str(due_at), "%Y-%m-%d %H:%M")
        except ValueError:
            return ""

        delta = due_time - datetime.now()
        total_minutes = int(delta.total_seconds() // 60)
        if total_minutes < 0:
            return f"已超时 {abs(total_minutes)} 分钟"
        if total_minutes < 60:
            return f"剩余 {total_minutes} 分钟"
        hours, minutes = divmod(total_minutes, 60)
        return f"剩余 {hours} 小时 {minutes} 分钟"


    def _render_task_preview(self, tasks, empty_text, highlight_color):
        if not tasks:
            print(self._paint(f"  {empty_text}", self.DIM))
            return

        for task in tasks[:3]:
            remaining = self._format_remaining(task.due_at)
            remainder_text = f" | {remaining}" if remaining else ""
            title = self._truncate(task.title, 20)
            due_at = self._truncate(str(task.due_at), 16)
            line = f"  • {title}  {due_at}{remainder_text}"
            print(self._paint(line, highlight_color))


    def _render_task_choices(self, tasks, empty_text):
        if not tasks:
            print(self._paint(f"  {empty_text}", self.DIM))
            return

        for index, task in enumerate(tasks, start=1):
            status_color = self.GREEN if str(task.status) in ["done", "已完成"] else self.YELLOW
            status_text = self._paint(self._truncate(task.status, 8), status_color)
            task_id_text = self._pad(task.id, 3)
            title = self._truncate(task.title, 18)
            due_at = self._truncate(str(task.due_at), 16)
            print(self._paint(f"  [ID {task_id_text}] | {title} | {status_text} | {due_at}", self.WHITE))


    def _render_task_table_header(self):
        print(
            self._paint(f"{'ID':<4}{'TITLE':<10}{'STATUS':<6}{'P':<2}{'CATEGORY':<6}{'TAGS':<8}{'DUE_TIME':<16}{'DONE_AT':<16}", self.BOLD)
        )
        print(self._paint("-" * 68, self.DIM))


    def _format_task_time(self, value, width):
        return self._truncate("" if value is None else value, width)


    def _render_task_summary_header(self):
        print(
            self._paint(f"{'ID':<4}{'TITLE':<24}{'STATUS':<8}{'CATEGORY':<10}{'DUE_TIME':<16}", self.BOLD)
        )
        print(self._paint("-" * 62, self.DIM))


    def _render_task_summary_row(self, task):
        status_color = self.GREEN if str(task.status) in ["done", "已完成"] else self.YELLOW
        category_color = self.CYAN if task.category else self.DIM

        print(
            self._truncate(task.id, 4)
            + self._truncate(task.title, 24)
            + self._paint(self._truncate(task.status, 8), status_color)
            + self._paint(self._truncate(task.category, 10), category_color)
            + self._format_task_time(task.due_at, 16)
        )


    def _render_task_detail(self, task):
        self._render_title("任务详情")
        print(self._paint(f"ID: {task.id}", self.WHITE))
        print(self._paint(f"标题: {task.title}", self.WHITE))
        print(self._paint(f"状态: {task.status}", self.WHITE))
        print(self._paint(f"优先级: {task.priority}", self.WHITE))
        print(self._paint(f"种类: {task.category or '无'}", self.WHITE))
        print(self._paint(f"标签: {', '.join(task.tags) if task.tags else '无'}", self.WHITE))
        print(self._paint(f"创建时间: {task.created_at or '无'}", self.WHITE))
        print(self._paint(f"截止时间: {task.due_at or '无'}", self.WHITE))
        print(self._paint(f"完成时间: {task.completed_at or '无'}", self.WHITE))


    def _render_task_table_row(self, task):
        status_color = self.GREEN if str(task.status) in ["done", "已完成"] else self.YELLOW
        category_color = self.CYAN if task.category else self.DIM
        tags_text = ", ".join(task.tags)

        print(
            self._truncate(task.id, 4)
            + self._truncate(task.title, 10)
            + self._paint(self._truncate(task.status, 6), status_color)
            + self._truncate(task.priority, 2)
            + self._paint(self._truncate(task.category, 6), category_color)
            + self._truncate(tags_text, 8)
            + self._format_task_time(task.due_at, 16)
            + self._format_task_time(task.completed_at, 16)
        )


    def _select_task_id(self, tasks, prompt, empty_text="暂无可选任务", full_table=False, render=True):
        if render and full_table:
            if not tasks:
                print(self._paint(f"  {empty_text}", self.DIM))
                return None

            self._render_task_table_header()
            for task in tasks:
                self._render_task_table_row(task)
        elif render:
            self._render_task_choices(tasks, empty_text)

        choice = input(prompt).strip()
        if choice == "":
            return None

        for task in tasks:
            if str(task.id) == choice:
                return choice

        print(self._paint("ID 无效，请重新输入。", self.RED))
        self.pause()
        return None


    def _select_from_list(self, items, prompt, empty_text, title):
        if not items:
            print(self._paint(f"  {empty_text}", self.DIM))
            self.pause()
            return None

        self._render_section_title(title, self.CYAN)
        for index, item in enumerate(items, start=1):
            print(self._paint(f"  [{index}] {item}", self.DIM))

        choice = input(prompt).strip()
        if choice == "":
            return None

        try:
            index = int(choice)
        except ValueError:
            print(self._paint("选择无效，请重新输入。", self.RED))
            self.pause()
            return None

        if not (1 <= index <= len(items)):
            print(self._paint("选择无效，请重新输入。", self.RED))
            self.pause()
            return None

        return items[index - 1]


    def _input_tags_for_update(self):
        existing_tags = self.task_service.list_all_tags()

        self._render_section_title("已有标签", self.CYAN)
        if existing_tags:
            for index, tag in enumerate(existing_tags, start=1):
                print(self._paint(f"  [{index}] {tag}", self.DIM))
        else:
            print(self._paint("  当前没有已有标签。", self.DIM))

        self._render_menu("更新标签", [
            ("1", "从已有标签中选择"),
            ("2", "创建新标签"),
            ("0", "返回"),
        ])
        choice = input("选择: ").strip()

        if choice == "0":
            return None

        if choice == "1":
            if not existing_tags:
                print(self._paint("当前没有可选标签，请先创建标签。", self.YELLOW))
                self.pause()
                return None

            print(self._paint("输入标签编号，多个编号用空格分隔。", self.DIM))
            raw_indexes = input("标签编号: ").strip()
            if not raw_indexes:
                return None

            selected_tags = []
            for raw_index in raw_indexes.split():
                try:
                    index = int(raw_index)
                except ValueError:
                    print(self._paint("标签编号无效，请重新输入。", self.RED))
                    self.pause()
                    return None

                if not (1 <= index <= len(existing_tags)):
                    print(self._paint("标签编号无效，请重新输入。", self.RED))
                    self.pause()
                    return None

                tag = existing_tags[index - 1]
                if tag not in selected_tags:
                    selected_tags.append(tag)

            return selected_tags

        if choice == "2":
            print(self._paint("输入新标签名称，多个标签用空格分隔。", self.DIM))
            new_tags = input("新标签: ").strip()
            if not new_tags:
                return None
            return new_tags

        print(self._paint("错误指令", self.RED))
        self.pause()
        return None


    def _render_task_context(self, task):
        category_text = task.category if task and task.category else "无"
        tags_text = ", ".join(task.tags) if task and task.tags else "无"
        print(self._paint(f"当前种类: {category_text}", self.CYAN))
        print(self._paint(f"当前标签: {tags_text}", self.CYAN))


    def _render_update_resources(self):
        print(self._paint("可选种类:", self.CYAN))
        for index, category in enumerate(service_helper.ALLOWED_CATEGORIES, start=1):
            print(self._paint(f"  [{index}] {category}", self.DIM))

        print(self._paint("已有标签:", self.CYAN))
        existing_tags = self.task_service.list_all_tags()
        if existing_tags:
            for index, tag in enumerate(existing_tags, start=1):
                print(self._paint(f"  [{index}] {tag}", self.DIM))
        else:
            print(self._paint("  当前没有已有标签。", self.DIM))


    def _render_title(self, title):
        width = self._menu_width
        line = "═" * width
        title_text = f" {title} "
        left = max((width - wcswidth(title_text)) // 2, 0)
        right = max(width - left - wcswidth(title_text), 0)
        print(self._paint(f"╔{line}╗", self.CYAN))
        print(self._paint(f"{' ' * left}{title_text}{' ' * right}", self.BOLD + self.WHITE))
        print(self._paint(f"╚{line}╝", self.CYAN))


    def _render_dashboard(self):
        stats = self.task_service.get_stats()
        due_soon_tasks = self.task_service.list_due_soon()

        print(self._paint(self._box_line("任务概览", now()), self.BLUE))
        print(self._paint(self._box_line(f"总任务 {stats['all']}", f"已完成 {stats['done']} / 未完成 {stats['todo']}"), self.DIM))
        print(self._paint("─" * self._menu_width, self.BLUE))
        self._render_section_title("24 小时内到期提醒", self.YELLOW)
        self._render_task_preview(due_soon_tasks, "暂无即将到期的任务。", self.YELLOW)
        print(self._paint("─" * self._menu_width, self.BLUE))


    def _render_menu(self, title, items):
        self._render_title(title)
        for key, label in items:
            print(self._paint(f"  [{key}]  {label}", self.WHITE))
        print(self._paint("─" * self._menu_width, self.BLUE))


    def _dispatch_choice(self, choice, actions):
        action = actions.get(choice)
        if action is None:
            print(self._paint("错误指令", self.RED))
            self.pause()
            return False

        action()
        return True


    def _show_message(self, message, color=None):
        if message:
            print(self._paint(message, color or self.GREEN))
            self.pause()


    def _truncate(self, text, width):
        text = "" if text is None else str(text)
        if wcswidth(text) <= width:
            return text + " " * (width - wcswidth(text))

        result = ""
        current_width = 0
        for char in text:
            char_width = wcswidth(char)
            if current_width + char_width > width - 1:
                break
            result += char
            current_width += char_width
        return result + "…" + " " * max(width - current_width - 1, 0)


    def _wrap_text(self, text, width):
        text = "" if text is None else str(text)
        if not text:
            return [""]

        lines = []
        current_line = ""
        current_width = 0

        for char in text:
            char_width = wcswidth(char)
            if current_line and current_width + char_width > width:
                lines.append(current_line)
                current_line = char
                current_width = char_width
            else:
                current_line += char
                current_width += char_width

        if current_line or not lines:
            lines.append(current_line)

        return lines


    def _pad(self, text, width):
        text = str(text)
        real_len = wcswidth(text)
        space = width - real_len
        return text + " " * max(space, 0)


    def handle_app_error(self, error, source):
        logger.error("操作失败 | source=%s | error=%s", source, str(error))
        print(self._paint(f"操作失败：{error}", self.RED))
        self.pause()


    def pause(self):
        input(self._paint("\n按回车键继续...", self.DIM))


    def show_tasks(self, tasks):
        if not tasks:
            self._render_title("任务列表")
            print(self._paint("暂无任务", self.YELLOW))
            self.pause()
            return

        self._render_title("任务列表")
        self._render_task_summary_header()
        for task in tasks:
            self._render_task_summary_row(task)

        task_id = self._select_task_id(tasks, "输入任务ID查看详情(回车返回): ", render=False)
        if not task_id:
            return

        task = self.task_service.get_task_by_id(task_id)
        if task:
            self._clear_screen()
            self._render_task_detail(task)
            self.pause()
            return

        print(self._paint("任务不存在。", self.RED))
        self.pause()


    def main_menu(self):
        while True:
            self._clear_screen()
            self._render_dashboard()
            self._render_menu("TodoList", [
                ("1", "添加任务"),
                ("2", "查看任务"),
                ("3", "更新任务"),
                ("4", "完成 / 撤销任务"),
                ("5", "删除任务"),
                ("6", "AI分析今日任务"),
                ("0", "退出程序"),
            ])

            cmd = input("选择: ").strip()

            if cmd == "0":
                self._clear_screen()
                break

            self._dispatch_choice(cmd, {
                "1": self.add_task_menu,
                "2": self.tasks_menu,
                "3": self.update_task_menu,
                "4": self.done_task_menu,
                "5": self.delete_task_menu,
                "6": self.analyze_today_tasks_menu,
            })


    def analyze_today_tasks_menu(self):
        self._clear_screen()
        self._render_title("AI分析今日任务")

        try:
            analysis = self.task_service.analyze_today_tasks()
            print(self._paint(analysis, self.GREEN))
            self.pause()
        except AppError as error:
            self.handle_app_error(error, "AI分析今日任务")
        except Exception as error:
            logger.error("AI分析今日任务失败 | error=%s", str(error))
            print(self._paint(f"AI分析失败：{error}", self.RED))
            self.pause()


    def tasks_menu(self):
        while True:
            self._clear_screen()
            self._render_menu("任务查看", [
                ("1", "全部任务"),
                ("2", "今日任务"),
                ("3", "代办任务"),
                ("4", "优先任务"),
                ("5", "过期任务"),
                ("6", "统计数据"),
                ("7", "搜索任务"),
                ("8", "根据种类查看任务"),
                ("9", "根据标签查看任务"),
                ("0", "返回"),
            ])
            choice = input("选择: ").strip()

            try:
                if choice == "0":
                    break

                def show_priority_tasks():
                    min_priority = input("最低优先级: ")
                    max_priority = input("最高优先级: ")
                    self.show_tasks(self.task_service.list_priority(min_priority, max_priority))

                def search_tasks():
                    keyword = input("关键词: ")
                    result = self.task_service.search_task(keyword)
                    if result:
                        self.show_tasks(result)
                    else:
                        print(self._paint("未找到匹配任务", self.YELLOW))
                        self.pause()

                def show_categories():
                    categories = service_helper.ALLOWED_CATEGORIES
                    category = self._select_from_list(categories, "任务种类编号: ", "当前没有可选种类", "可用的任务种类")
                    if category is not None:
                        self.show_tasks(self.task_service.list_by_category(category))

                def show_tags():
                    print(self._paint("可用的标签:", self.CYAN))
                    for tag in self.task_service.list_all_tags():
                        print(self._paint(f"  - {tag}", self.DIM))
                    tag = input("标签: ")
                    self.show_tasks(self.task_service.list_by_tag(tag))

                handled = self._dispatch_choice(choice, {
                    "1": lambda: self.show_tasks(self.task_service.list_tasks()),
                    "2": lambda: self.show_tasks(self.task_service.list_today()),
                    "3": lambda: self.show_tasks(self.task_service.list_todo()),
                    "4": show_priority_tasks,
                    "5": lambda: self.show_tasks(self.task_service.list_overdue()),
                    "6": self.show_stats,
                    "7": search_tasks,
                    "8": show_categories,
                    "9": show_tags,
                })

                if handled:
                    continue
            except AppError as error:
                self.handle_app_error(error, "查看任务")


    def add_task_menu(self):
        self._clear_screen()
        self._render_title("添加任务")
        print(self._paint("提示：可以直接输入自然语言，也可以按回车后逐项填写。", self.DIM))
        text = input("输入自然语言(按回车键跳过): ")
        if not text.strip():
            title = input("任务标题: ")
            priority = input("优先级(0~5): ")
            due_at = input("截止时间: ")

        try:
            if text.strip():
                message = self.task_service.add_task_by_ai(text)
            else:
                message = self.task_service.add_task(title, priority, due_at)
            self._show_message(message, self.GREEN)
        except AppError as error:
            self.handle_app_error(error, "添加任务")


    def update_task_menu(self):
        self._clear_screen()
        try:
            tasks = self.task_service.list_tasks()
            self._render_title("更新任务")
            self._render_task_table_header()
            for task in tasks:
                self._render_task_table_row(task)

            task_id = self._select_task_id(tasks, "输入任务ID(回车返回): ", "当前没有任务可更新", render=False)
            if not task_id:
                return

            self._render_menu("更新任务", [
                ("1", "修改任务标题"),
                ("2", "修改截止时间"),
                ("3", "修改任务优先级"),
                ("4", "修改任务种类"),
                ("5", "修改任务标签"),
                ("0", "返回"),
            ])
            choice = input("选择: ").strip()

            if choice == "0":
                return

            actions = {
                "1": lambda: self._show_message(self.task_service.update_title(task_id, input("更新标题: "))),
                "2": lambda: self._show_message(self.task_service.update_due_at(task_id, input("更新时间: "))),
                "3": lambda: self._show_message(self.task_service.update_priority(task_id, input("更新优先级: "))),
                "4": lambda: self._update_category_for_task(task_id),
                "5": lambda: self._update_tags_for_task(task_id),
            }
            self._dispatch_choice(choice, actions)
        except AppError as error:
            self.handle_app_error(error, "更新任务")


    def _update_category_for_task(self, task_id):
        categories = service_helper.ALLOWED_CATEGORIES
        category = self._select_from_list(categories, "分类编号: ", "当前没有可选种类", "可用的任务种类")
        if category is None:
            return

        self._show_message(self.task_service.update_category(task_id, category))


    def _update_tags_for_task(self, task_id):
        task = self.task_service.get_task_by_id(task_id)
        self._render_task_context(task)

        tags = self._input_tags_for_update()
        if tags is None:
            return

        self._show_message(self.task_service.update_tags(task_id, tags))


    def done_task_menu(self):
        self._clear_screen()
        self._render_menu("任务状态", [
            ("1", "完成任务"),
            ("2", "撤销完成任务"),
            ("0", "返回"),
        ])
        try:
            choice = input("选择: ").strip()
            if choice == "0":
                return

            if choice == "1":
                task_id = self._select_task_id(
                    self.task_service.list_todo(),
                    "输入任务ID完成: ",
                    "当前没有待完成任务",
                )
                if task_id:
                    self._show_message(self.task_service.done_task(task_id))
            elif choice == "2":
                task_id = self._select_task_id(
                    self.task_service.list_done(),
                    "输入任务ID撤销: ",
                    "当前没有已完成任务",
                )
                if task_id:
                    self._show_message(self.task_service.undo_task(task_id))
            else:
                print(self._paint("错误指令", self.RED))
                self.pause()
        except AppError as error:
            self.handle_app_error(error, "完成/撤销任务")


    def delete_task_menu(self):
        self._clear_screen()
        self._render_title("删除任务")
        try:
            task_id = self._select_task_id(
                self.task_service.list_tasks(),
                "输入任务ID删除: ",
                "当前没有任务可删除",
            )
            if task_id:
                message = self.task_service.delete_task(task_id)
                self._show_message(message, self.GREEN)
        except AppError as error:
            self.handle_app_error(error, "删除任务")


    def show_stats(self):
        self._render_title("统计数据")
        stats = self.task_service.get_stats()
        print(self._paint(self._box_line("任务统计", now()), self.BLUE))
        print(self._paint(self._box_line(f"总任务 {stats['all']}", f"已完成 {stats['done']} / 待办 {stats['todo']}"), self.DIM))
        print(self._paint("─" * self._menu_width, self.BLUE))
        self.pause()