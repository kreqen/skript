"""Виджет заголовка приложения."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.constants import APP_DESCRIPTION, APP_NAME, COLORS
from app.ui.styles import HEADER_STYLESHEET, NAV_BUTTON_STYLESHEET


class HeaderWidget(QWidget):
    """Заголовочный виджет приложения."""

    def __init__(self, parent=None) -> None:
        """Инициализировать заголовок."""
        super().__init__(parent)
        self.setStyleSheet(HEADER_STYLESHEET)
        self.setMinimumHeight(80)

        layout = QHBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(20, 15, 20, 15)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        app_name = QLabel(APP_NAME)
        app_name.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {COLORS['pink_bright']};"
        )

        app_desc = QLabel(APP_DESCRIPTION)
        app_desc.setObjectName("subtitle")
        app_desc.setStyleSheet(f"font-size: 11px; color: {COLORS['text_secondary']};")

        title_layout.addWidget(app_name)
        title_layout.addWidget(app_desc)

        layout.addLayout(title_layout)
        layout.addStretch()

        self.nav_buttons = {}
        nav_items = [("solver", "Решение"), ("history", "История"), ("settings", "Настройки")]

        for key, text in nav_items:
            btn = QPushButton(text)
            btn.setStyleSheet(NAV_BUTTON_STYLESHEET)
            btn.setMinimumWidth(100)
            btn.setMinimumHeight(40)
            btn.setCheckable(True)
            btn.setFlat(True)
            self.nav_buttons[key] = btn
            layout.addWidget(btn)

        self.nav_buttons["solver"].setChecked(True)
