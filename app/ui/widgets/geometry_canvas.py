from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from app.services.geometry_service import GeometryService


class GeometryCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.geometry_service = GeometryService()

        self.figure = None
        self.canvas = None

        self.layout = QVBoxLayout(self)

        self.save_button = QPushButton("Сохранить рисунок")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

    def clear(self):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None
            self.figure = None

    def draw_geometry(self, geometry_data):
        self.clear()
        self.figure = self.geometry_service.create_figure(geometry_data)
        self.canvas = FigureCanvas(self.figure)
        self.layout.insertWidget(0, self.canvas)
        self.canvas.draw()

    def save_image(self):
        if not self.figure:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить рисунок", "", "PNG Files (*.png)"
        )
        if file_path:
            self.figure.savefig(file_path, facecolor=self.figure.get_facecolor())