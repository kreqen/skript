"""Сервис для работы с историей решений."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import HISTORY_FILE_PATH


class HistoryService:
    """Сервис для работы с историей решений."""

    def __init__(self) -> None:
        """Инициализировать сервис."""
        self.history_file = HISTORY_FILE_PATH
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Убедиться, что файл истории существует."""
        if not self.history_file.exists():
            self.history_file.write_text("[]", encoding="utf-8")

    def add_solution(
        self,
        subject: str,
        task_text: str,
        short_answer: str,
        full_solution: str,
        image_path: Optional[str] = None,
    ) -> bool:
        """Добавить решение в историю."""
        try:
            history = self.load_history()

            entry = {
                "subject": subject,
                "task_text": task_text,
                "short_answer": short_answer,
                "full_solution": full_solution,
                "image_path": image_path,
                "created_at": datetime.now().isoformat(),
            }

            history.append(entry)
            self._save_history(history)
            return True
        except Exception:
            return False

    def load_history(self) -> list[dict]:
        """Загрузить историю из файла."""
        try:
            self._ensure_history_file()
            content = self.history_file.read_text(encoding="utf-8")
            if not content.strip():
                return []
            return json.loads(content)
        except (json.JSONDecodeError, OSError):
            return []

    def _save_history(self, history: list[dict]) -> None:
        """Сохранить историю в файл."""
        self.history_file.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def clear_history(self) -> bool:
        """Очистить всю историю."""
        try:
            self._save_history([])
            return True
        except Exception:
            return False

    def get_entry(self, index: int) -> Optional[dict]:
        """Получить запись истории по индексу."""
        history = self.load_history()
        if 0 <= index < len(history):
            return history[index]
        return None

    def delete_entry(self, index: int) -> bool:
        """Удалить запись истории по индексу."""
        try:
            history = self.load_history()
            if 0 <= index < len(history):
                history.pop(index)
                self._save_history(history)
                return True
            return False
        except Exception:
            return False
