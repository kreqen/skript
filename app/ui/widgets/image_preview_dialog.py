"""Диалог для просмотра изображения задачи."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

from app.constants import COLORS
from app.ui.widgets.gradient_button import GradientButton


class ImagePreviewDialog(QDialog):
    """Диалог для просмотра полноразмерного изображения задачи."""

    def __init__(self, image_path: str, parent=None) -> None:
        """Инициализировать диалог просмотра.
        
        Args:
            image_path: путь к файлу изображения
            parent: родительский виджет
        """
        super().__init__(parent)
        self.setWindowTitle("Просмотр изображения задачи")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(f"background-color: {COLORS['bg_primary']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Область с изображением
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(f"background-color: {COLORS['bg_secondary']};")

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self._original_pixmap = pixmap
            scaled = pixmap.scaledToWidth(
                550,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled)
        else:
            self._original_pixmap = None
            self.image_label.setText("Не удалось загрузить изображение")
            self.image_label.setStyleSheet(
                f"background-color: {COLORS['bg_secondary']}; "
                f"color: {COLORS['text_secondary']};"
            )

        layout.addWidget(self.image_label, 1)

        # Кнопка закрытия
        button_layout = QHBoxLayout()
        close_button = GradientButton("Закрыть")
        close_button.setMaximumWidth(120)
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

    def resizeEvent(self, event) -> None:
        """Масштабировать изображение при изменении размера окна."""
        super().resizeEvent(event)
        # Перемасштабировать pixmap, если изображение было загружено
        if hasattr(self, "_original_pixmap"):
            new_width = self.width() - 40
            scaled = self._original_pixmap.scaledToWidth(
                new_width,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled)
