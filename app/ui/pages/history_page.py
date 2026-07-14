"""Страница истории решений."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from app.constants import COLORS
from app.ui.widgets.gradient_button import GradientButton


class HistoryPage(QWidget):
    """Страница с историей решений."""

    def __init__(self, parent=None) -> None:
        """Инициализировать страницу истории."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        history_label = QLabel("История решений")
        history_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['text_primary']};")
        left_layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        left_layout.addWidget(self.history_list)

        clear_layout = QHBoxLayout()
        self.clear_history_button = GradientButton("Очистить историю", is_secondary=True)
        self.clear_history_button.setMaximumWidth(160)
        clear_layout.addWidget(self.clear_history_button)
        clear_layout.addStretch()
        left_layout.addLayout(clear_layout)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        detail_label = QLabel("Детали")
        detail_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {COLORS['text_primary']};")
        right_layout.addWidget(detail_label)

        self.detail_view = QTextEdit()
        self.detail_view.setReadOnly(True)
        self.detail_view.setPlaceholderText("Выберите запись из истории для просмотра подробностей")
        right_layout.addWidget(self.detail_view)

        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 1)

    def on_history_item_clicked(self, item: QListWidgetItem) -> None:
        """Обработать клик по записи истории."""
        pass

    def set_empty_message(self) -> None:
        """Показать сообщение об пустой истории."""
        self.history_list.clear()
        self.detail_view.clear()
        empty_item = QListWidgetItem("История пуста")
        empty_item.setFlags(empty_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.history_list.addItem(empty_item)

    def load_history(self, history: list[dict]) -> None:
        """Заполнить список истории."""
        self.history_list.clear()
        self.detail_view.clear()

        if not history:
            self.set_empty_message()
            return

        for entry in history:
            created_at = entry.get("created_at", "?")
            subject = entry.get("subject", "Неизвестно")
            source = entry.get("source") or (
                "Текст и изображение"
                if entry.get("task_text") and entry.get("image_path")
                else "Изображение"
                if entry.get("image_path")
                else "Текст"
            )
            item_text = f"{created_at[:10]} — {subject} — {source}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.history_list.addItem(item)

    def on_history_item_clicked(self, item: QListWidgetItem) -> None:
        """Обработать клик по записи истории."""
        entry = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(entry, dict):
            return

        image_path = entry.get("image_path")
        if image_path and not Path(image_path).exists():
            image_status = "Файл изображения больше не найден"
        elif image_path:
            image_status = image_path
        else:
            image_status = "Изображение отсутствует"

        source = entry.get("source") or (
            "Текст и изображение"
            if entry.get("task_text") and entry.get("image_path")
            else "Изображение"
            if entry.get("image_path")
            else "Текст"
        )

        detail_lines = [
            f"Дата: {entry.get('created_at', 'Неизвестно')}",
            f"Предмет: {entry.get('subject', 'Неизвестно')}",
            f"Источник задачи: {source}",
            "",
            "Условие задачи:",
            entry.get("task_text", ""),
            "",
            f"Изображение: {image_status}",
            "",
            "Краткий ответ:",
            entry.get("short_answer", ""),
            "",
            "Полное решение:",
            entry.get("full_solution", ""),
        ]

        self.detail_view.setPlainText("\n".join(detail_lines))
