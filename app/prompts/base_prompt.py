"""Базовый системный промпт для решения задач."""

from app.constants import SCHOOL_SOLVER_SYSTEM_PROMPT


class BasePrompt:
    """Общий системный промпт для AI-решений."""

    @staticmethod
    def get_system_prompt() -> str:
        return SCHOOL_SOLVER_SYSTEM_PROMPT

    @staticmethod
    def get_detailed_mode_instruction(enabled: bool) -> str:
        if enabled:
            return (
                "Предоставь подробное пошаговое решение с пояснениями каждой стадии "
                "и разъясни, почему выбранные формулы применяются."
            )
        return (
            "Дай ясное и понятное решение без лишних подробностей, но с достаточными шагами."
        )
