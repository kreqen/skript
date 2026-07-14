"""Панель результатов решения."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QScrollArea,
)

from app.constants import COLORS
from app.ui.widgets.gradient_button import GradientButton


class ResultPanel(QWidget):
    """Панель для отображения результатов."""

    def __init__(self, parent=None) -> None:
        """Инициализировать панель результатов."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Результат")
        title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLORS['text_primary']};")
        layout.addWidget(title)

        self.answer_output = QTextEdit()
        self.answer_output.setReadOnly(True)
        self.answer_output.setPlaceholderText("Здесь появится результат решения...")
        self.answer_output.setMinimumHeight(250)
        layout.addWidget(self.answer_output)

        button_layout = QHBoxLayout()
        self.copy_button = GradientButton("Копировать", is_secondary=True)
        self.copy_button.setMaximumWidth(120)
        button_layout.addWidget(self.copy_button)

        self.save_button = GradientButton("Сохранить", is_secondary=True)
        self.save_button.setMaximumWidth(120)
        button_layout.addWidget(self.save_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        geom_label = QLabel("Геометрический рисунок:")
        geom_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(geom_label)

        self.geometry_area = QLabel()
        self.geometry_area.setMinimumHeight(200)
        self.geometry_area.setStyleSheet(
            f"background-color: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px;"
        )
        self.geometry_area.setText("Рисунок появится здесь")
        layout.addWidget(self.geometry_area)

        self.demo_figure_button = GradientButton("Показать пример рисунка", is_secondary=True)
        self.demo_figure_button.setMaximumWidth(200)
        layout.addWidget(self.demo_figure_button)

        self.status_label = QLabel("Готово")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        layout.addWidget(self.status_label)

        layout.addStretch()
