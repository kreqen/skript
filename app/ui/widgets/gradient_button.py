"""Кнопка с градиентом."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from app.ui.styles import GRADIENT_BUTTON_STYLESHEET, SECONDARY_BUTTON_STYLESHEET


class GradientButton(QPushButton):
    """Кнопка с розовым градиентом."""

    def __init__(self, text: str, parent=None, is_secondary: bool = False) -> None:
        """Инициализировать кнопку."""
        super().__init__(text, parent)
        if is_secondary:
            self.setStyleSheet(SECONDARY_BUTTON_STYLESHEET)
        else:
            self.setStyleSheet(GRADIENT_BUTTON_STYLESHEET)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
