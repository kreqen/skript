from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImagePreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #111116;
            color: white;
            font-family: Arial, sans-serif;
        """)

        self.layout = QVBoxLayout(self)

        self.image_label = QLabel("Фото задачи не выбрано")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.delete_image_button = QPushButton("Удалить фото")
        self.layout.addWidget(self.delete_image_button)

        # Add preview_area attribute as alias to image_label for compatibility
        self.preview_area = self.image_label

    def show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Не удалось загрузить изображение")
        else:
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def clear(self):
        self.image_label.setText("Фото задачи не выбрано")
        self.image_label.setPixmap(QPixmap())
        self.delete_image_button.setEnabled(False)