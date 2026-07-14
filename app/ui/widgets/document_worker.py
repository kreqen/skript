from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from app.services.document_service import DocumentService
from app.models.document import DocumentContent

class DocumentWorkerSignals(QObject):
    finished = Signal(DocumentContent)
    error = Signal(str)

class DocumentWorker(QRunnable):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.signals = DocumentWorkerSignals()
        self.document_service = DocumentService()

    @Slot()
    def run(self):
        try:
            document_content = self.document_service.extract_document(self.file_path)
            self.signals.finished.emit(document_content)
        except Exception as e:
            self.signals.error.emit(str(e))