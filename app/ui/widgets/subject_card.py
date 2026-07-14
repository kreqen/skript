"""Карточка выбора предмета."""

from PySide6.QtWidgets import QPushButton

from app.ui.styles import SUBJECT_CARD_STYLESHEET


class SubjectCard(QPushButton):
    """Карточка предмета для выбора."""

    def __init__(self, subject_name: str, parent=None) -> None:
        """Инициализировать карточку предмета."""
        super().__init__(subject_name, parent)
        self.subject_name = subject_name
        self.setStyleSheet(SUBJECT_CARD_STYLESHEET)
        self.setCheckable(True)
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
