"""Страница настроек приложения."""

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from app.constants import COLORS
from app.ui.widgets.gradient_button import GradientButton


class SettingsPage(QWidget):
    """Страница настроек приложения."""

    def __init__(self, parent=None) -> None:
        """Инициализировать страницу настроек."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Настройки")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLORS['text_primary']};"
        )
        layout.addWidget(title)

        mode_label = QLabel("Режим работы:")
        mode_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(mode_label)

        self.api_mode_combo = QComboBox()
        self.api_mode_combo.addItems(["Тестовый режим", "OpenAI API"])
        self.api_mode_combo.setMinimumHeight(34)
        layout.addWidget(self.api_mode_combo)

        note_label = QLabel(
            "В режиме OpenAI API запросы могут расходовать средства API-баланса."
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        layout.addWidget(note_label)

        model_label = QLabel("Модель OpenAI:")
        model_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(model_label)

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("gpt-4.1-mini")
        layout.addWidget(self.model_input)

        api_label = QLabel("API-ключ OpenAI:")
        api_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(api_label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Введите ваш API-ключ")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.api_key_input)

        key_button_layout = QHBoxLayout()
        self.toggle_key_visibility_button = GradientButton("Показать ключ", is_secondary=True)
        self.toggle_key_visibility_button.setMaximumWidth(160)
        key_button_layout.addWidget(self.toggle_key_visibility_button)

        self.check_connection_button = GradientButton("Проверить подключение", is_secondary=True)
        self.check_connection_button.setMaximumWidth(190)
        key_button_layout.addWidget(self.check_connection_button)

        key_button_layout.addStretch()
        layout.addLayout(key_button_layout)

        self.connection_status_label = QLabel("Статус подключения: не проверено")
        self.connection_status_label.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 11px;"
        )
        layout.addWidget(self.connection_status_label)

        self.verbose_checkbox = QCheckBox("Показывать подробное решение")
        self.verbose_checkbox.setChecked(True)
        layout.addWidget(self.verbose_checkbox)

        self.auto_save_checkbox = QCheckBox("Автоматически сохранять в историю")
        self.auto_save_checkbox.setChecked(True)
        layout.addWidget(self.auto_save_checkbox)

        lang_label = QLabel("Язык интерфейса:")
        lang_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(lang_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        layout.addWidget(self.language_combo)

        layout.addSpacing(20)

        button_layout = QHBoxLayout()
        self.save_settings_button = GradientButton("Сохранить настройки")
        self.save_settings_button.setMaximumWidth(180)
        button_layout.addWidget(self.save_settings_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        layout.addStretch()
