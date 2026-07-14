"""Страница решения задач."""

from PySide6.QtWidgets import QHBoxLayout, QWidget

from app.ui.widgets import InputPanel, ResultPanel
from app.ui.widgets.geometry_canvas import GeometryCanvas


class SolverPage(QWidget):
    """Страница для решения задач."""

    def __init__(self, parent=None) -> None:
        """Инициализировать страницу решения."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        self.input_panel = InputPanel()
        self.result_panel = ResultPanel()
        self.geometry_canvas = GeometryCanvas()

        layout.addWidget(self.input_panel, 1)
        layout.addWidget(self.result_panel, 1)
        layout.addWidget(self.geometry_canvas, 1)

    def clear(self):
        self.geometry_canvas.clear()

    def display_solution(self, solution):
        geometry_data = getattr(solution, "geometry_data", None)
        if geometry_data:
            self.geometry_canvas.draw_geometry(geometry_data)
        else:
            self.geometry_canvas.clear()

    def show_analysis_message(self, message: str):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Анализ рисунка", message)

    def show_analysis_success(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Анализ рисунка", "Рисунок успешно распознан")
