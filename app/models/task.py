"""Модель задачи."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Task:
    """Класс, представляющий школьную задачу."""

    subject: str
    text: str
    image_path: Optional[str] = None
    document_path: Optional[str] = None
    document_content: Optional[str] = None
    document_type: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Инициализировать значения по умолчанию."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def has_image(self) -> bool:
        """Проверить, есть ли изображение в задаче."""
        if not self.image_path:
            return False
        return Path(self.image_path).exists()

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            "subject": self.subject,
            "text": self.text,
            "image_path": self.image_path,
            "document_path": self.document_path,
            "document_content": self.document_content,
            "document_type": self.document_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
