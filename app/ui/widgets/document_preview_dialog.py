from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class DocumentPreviewDialog(QDialog):
    def __init__(self, document_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предпросмотр документа")
        self.setMinimumSize(600, 600)
        self.setStyleSheet("""
            background-color: #111116;
            color: white;
            font-family: Arial, sans-serif;
        """)

        layout = QVBoxLayout(self)

        self.label_name = QLabel(f"Имя файла: {document_content.file_name}")
        self.label_type = QLabel(f"Тип файла: {document_content.file_type.upper()}")
        page_or_sheets = ""
        if document_content.page_count is not None:
            page_or_sheets = f"Количество страниц: {document_content.page_count}"
        elif document_content.sheet_names:
            page_or_sheets = f"Листы: {', '.join(document_content.sheet_names)}"
        self.label_pages = QLabel(page_or_sheets)

        layout.addWidget(self.label_name)
        layout.addWidget(self.label_type)
        layout.addWidget(self.label_pages)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(document_content.extracted_text)
        self.text_edit.setStyleSheet("""
            background-color: #222;
            color: white;
            font-family: Consolas, monospace;
        """)
        layout.addWidget(self.text_edit, 1)

        if document_content.warnings:
            self.label_warnings = QLabel("Предупреждения:\n" + "\n".join(document_content.warnings))
            self.label_warnings.setStyleSheet("color: #FF2E88;")
            layout.addWidget(self.label_warnings)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по тексту...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_layout.addWidget(self.search_input)

        self.copy_button = QPushButton("Копировать текст")
        self.copy_button.clicked.connect(self.copy_text)
        search_layout.addWidget(self.copy_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        search_layout.addItem(spacer)

        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)
        search_layout.addWidget(self.close_button)

        layout.addLayout(search_layout)

    def on_search_text_changed(self, text):
        cursor = self.text_edit.textCursor()
        document = self.text_edit.document()

        # Clear previous highlights
        extra_selections = []

        if text:
            highlight_color = Qt.yellow
            cursor = document.find(text, 0, Qt.CaseInsensitive)
            while not cursor.isNull():
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format.setBackground(highlight_color)
                extra_selections.append(selection)
                cursor = document.find(text, cursor.position(), Qt.CaseInsensitive)

        self.text_edit.setExtraSelections(extra_selections)

    def copy_text(self):
        self.text_edit.selectAll()
        self.text_edit.copy()