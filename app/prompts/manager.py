"""Менеджер промптов для различных типов задач и предметов."""

from app.models.task import Task
from app.prompts.base_prompt import BasePrompt
from app.prompts.subject_prompts import get_subject_instruction


class PromptManager:
    """Управляет системными и пользовательскими подсказками для AI."""

    def compose_system_instructions(self, task: Task, detailed: bool) -> str:
        """Сформировать системные инструкции для модели."""
        instructions = [BasePrompt.get_system_prompt()]
        instructions.append(get_subject_instruction(task.subject))
        instructions.append(BasePrompt.get_detailed_mode_instruction(detailed))

        if task.subject.strip().lower() == "автоматически":
            instructions.append(
                "Если не удаётся однозначно определить предмет, честно укажи это в поле \"detected_subject\"."
            )

        return "\n\n".join(instructions)

    def build_user_prompt(self, task: Task) -> str:
        """Сформировать текст для пользовательского запроса."""
        parts = [f"Выбранный предмет: {task.subject}"]

        if task.has_image():
            parts.append(
                "К задаче приложено изображение. Используй его совместно с текстом или комментариями пользователя."
            )

        if task.text.strip():
            parts.append("\nУсловие задачи:")
            parts.append(task.text.strip())
            if task.has_image():
                parts.append("\nКомментарий пользователя:")
                parts.append(task.text.strip())
        else:
            parts.append("\nУсловие задачи: см. изображение.")

        return "\n".join(parts)
