"""Модель решения."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Solution:
    """Класс, представляющий решение задачи."""

    subject: str
    short_answer: str
    detected_subject: str = ""
    steps: list[str] = field(default_factory=list)
    formulas: list[str] = field(default_factory=list)
    explanation: str = ""
    verification: str = ""
    source: str = "Текст"
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Инициализировать значения по умолчанию."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def format_as_text(self) -> str:
        """Форматировать решение в красивый текст."""
        lines = [f"Предмет: {self.subject}\n"]
        if self.detected_subject and self.detected_subject != self.subject:
            lines.insert(1, f"Определённый предмет: {self.detected_subject}\n")

        lines.append("Краткий ответ:")
        lines.append(self.short_answer + "\n")

        if self.steps:
            lines.append("Пошаговое решение:\n")
            for i, step in enumerate(self.steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        if self.formulas:
            lines.append("Формулы:")
            for formula in self.formulas:
                lines.append(f"• {formula}")
            lines.append("")
        else:
            lines.append("Формулы:")
            lines.append("Не потребовались.")
            lines.append("")

        if self.explanation:
            lines.append("Объяснение:")
            lines.append(self.explanation)
            lines.append("")

        if self.source:
            lines.insert(1, f"Источник задачи: {self.source}\n")

        if self.verification:
            lines.append("Проверка:")
            lines.append(self.verification)

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            "subject": self.subject,
            "detected_subject": self.detected_subject,
            "short_answer": self.short_answer,
            "steps": self.steps,
            "formulas": self.formulas,
            "explanation": self.explanation,
            "verification": self.verification,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
