from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout, QMessageBox, QTextEdit, QComboBox
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path
import os

from app.services.document_service import DocumentService
from app.ui.widgets.document_preview_dialog import DocumentPreviewDialog
from app.ui.widgets.gradient_button import GradientButton


class InputPanel(QWidget):
    document_loaded = Signal(object)  # Emits DocumentContent when document is loaded
    document_cleared = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.document_service = DocumentService()
        self.current_document = None

        self.layout = QVBoxLayout(self)

        # Task input
        self.task_input = QTextEdit()
        self.layout.addWidget(self.task_input)

        # Subject combo
        self.subject_combo = QComboBox()
        self.layout.addWidget(self.subject_combo)

        # Solve button
        self.solve_button = GradientButton("Решить задачу")
        self.layout.addWidget(self.solve_button)

        # Clear button
        self.clear_button = GradientButton("Очистить", is_secondary=True)
        self.layout.addWidget(self.clear_button)

        # Photo upload button
        self.photo_button = QPushButton("Загрузить фото")
        self.layout.addWidget(self.photo_button)

        # Remove photo button (added for compatibility)
        self.remove_photo_button = getattr(self, "remove_photo_button", None)
        if self.remove_photo_button is None:
            self.remove_photo_button = QPushButton("Удалить фото")
            self.layout.addWidget(self.remove_photo_button)

        # Document upload button
        self.document_button = QPushButton("Загрузить документ")
        self.document_button.clicked.connect(self.load_document)
        self.layout.addWidget(self.document_button)

        # Remove document button (added for compatibility)
        self.remove_document_button = getattr(self, "remove_document_button", None)
        if self.remove_document_button is None:
            self.remove_document_button = QPushButton("Удалить документ")
            self.layout.addWidget(self.remove_document_button)

        # Document info card widgets
        self.doc_info_widget = QWidget()
        self.doc_info_layout = QHBoxLayout(self.doc_info_widget)
        self.doc_info_label = QLabel()
        self.doc_delete_button = QPushButton("Удалить документ")
        self.doc_preview_button = QPushButton("Просмотреть текст")

        self.doc_info_layout.addWidget(self.doc_info_label)
        self.doc_info_layout.addWidget(self.doc_preview_button)
        self.doc_info_layout.addWidget(self.doc_delete_button)
        self.layout.addWidget(self.doc_info_widget)
        self.doc_info_widget.hide()

        self.doc_delete_button.clicked.connect(self.clear_document)
        self.doc_preview_button.clicked.connect(self.preview_document)

        # Image preview widget alias and delete button alias
        # Ensure image_preview exists for UI connections
        self.image_preview = getattr(self, "photo_preview", None)
        if self.image_preview is None:
            from app.ui.widgets.image_preview_widget import ImagePreviewWidget
            self.image_preview = ImagePreviewWidget()
            self.layout.addWidget(self.image_preview)
        if not hasattr(self.image_preview, "delete_image_button"):
            if hasattr(self.image_preview, "remove_button"):
                self.image_preview.delete_image_button = self.image_preview.remove_button

        # Document preview widget alias and delete button alias
        from app.ui.widgets.document_preview_dialog import DocumentPreviewDialog
        self._document_preview = None
        self.document_preview = self._document_preview
        # If you have a real document preview widget, assign it here instead of None
        # For now, create a placeholder widget with delete_document_button attribute
        class DummyDocumentPreview(QWidget):
            def __init__(self):
                super().__init__()
                self.delete_document_button = QPushButton("Удалить документ")
        if self.document_preview is None:
            self._document_preview = DummyDocumentPreview()
            self.document_preview = self._document_preview
        if not hasattr(self.document_preview, "delete_document_button"):
            if hasattr(self.document_preview, "remove_document_button"):
                self.document_preview.delete_document_button = self.document_preview.remove_document_button

    def load_document(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите документ", "", "Документы (*.pdf *.docx *.xlsx *.xlsm *.csv *.txt *.doc *.xls)"
        )
        if not file_path:
            return

        valid, message = self.document_service.validate_document(file_path)
        if not valid:
            QMessageBox.warning(self, "Ошибка загрузки документа", message)
            return

        # Запуск фонового воркера для извлечения документа
        from app.ui.widgets.document_worker import DocumentWorker
        self.document_button.setEnabled(False)
        self.doc_delete_button.setEnabled(False)
        self.doc_preview_button.setEnabled(False)

        self.worker = DocumentWorker(file_path)
        self.worker.signals.finished.connect(self.on_document_extracted)
        self.worker.signals.error.connect(self.on_document_error)

        from PySide6.QtCore import QThreadPool
        QThreadPool.globalInstance().start(self.worker)

    def on_document_extracted(self, document_content):
        self.current_document = document_content
        self.show_document_info()
        self.document_loaded.emit(document_content)
        self.document_button.setEnabled(True)
        self.doc_delete_button.setEnabled(True)
        self.doc_preview_button.setEnabled(True)

    def on_document_error(self, error_message):
        QMessageBox.warning(self, "Ошибка обработки документа", error_message)
        self.document_button.setEnabled(True)
        self.doc_delete_button.setEnabled(True)
        self.doc_preview_button.setEnabled(True)

    def show_document_info(self):
        if not self.current_document:
            self.doc_info_widget.hide()
            return
        info = f"{self.current_document.file_name} ({self.current_document.file_type.upper()})"
        if self.current_document.page_count:
            info += f", страниц: {self.current_document.page_count}"
        elif self.current_document.sheet_names:
            info += f", листов: {len(self.current_document.sheet_names)}"
        if self.current_document.warnings:
            info += " - Внимание: " + "; ".join(self.current_document.warnings)
        self.doc_info_label.setText(info)
        self.doc_info_widget.show()

    def clear_document(self):
        self.current_document = None
        self.doc_info_widget.hide()
        self.document_cleared.emit()

    def preview_document(self):
        if not self.current_document:
            return
        dialog = DocumentPreviewDialog(self.current_document, self)
        dialog.exec()

    def clear(self):
        # Clear document and other inputs if needed
        self.clear_document()
        self.task_input.clear()
        # Add clearing for image and other inputs if implemented
