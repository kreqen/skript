"""Главное окно приложения."""

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QStatusBar

from app.constants import WINDOW_DEFAULT_HEIGHT, WINDOW_DEFAULT_WIDTH
from app.ui.styles import MAIN_STYLESHEET
from app.ui.widgets import HeaderWidget
from app.ui.pages import SolverPage, HistoryPage, SettingsPage

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

class MainWindow(QMainWindow):
    """Главное окно приложения School AI Solver."""

    def __init__(self) -> None:
        """Инициализировать главное окно."""
        super().__init__()
        self.setWindowTitle("School AI Solver")
        self.setMinimumSize(1000, 700)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.setStyleSheet(MAIN_STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.header = HeaderWidget()
        main_layout.addWidget(self.header)

        self.pages = QStackedWidget()

        self.solver_page = SolverPage()
        self.history_page = HistoryPage()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.solver_page)
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.settings_page)

        main_layout.addWidget(self.pages, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

        self._connect_navigation()

        # Подключаем сигналы анализа рисунка
        self.solver_page.analysis_started = self._on_analysis_started
        self.solver_page.analysis_finished = self._on_analysis_finished

    def _connect_navigation(self) -> None:
        """Подключить навигацию между страницами."""
        for key, btn in self.header.nav_buttons.items():
            btn.clicked.connect(lambda checked, k=key: self._on_nav_click(k))

    def _on_nav_click(self, page_key: str) -> None:
        """Обработать клик по навигационной кнопке."""
        page_index = {"solver": 0, "history": 1, "settings": 2}.get(page_key, 0)
        self.pages.setCurrentIndex(page_index)

        for key, btn in self.header.nav_buttons.items():
            btn.setChecked(key == page_key)

    def _on_analysis_started(self):
        self.status_bar.showMessage("Анализируем рисунок...")

    def _on_analysis_finished(self, success: bool):
        if success:
            self.status_bar.showMessage("Рисунок успешно распознан")
        else:
            self.status_bar.showMessage("Не удалось полностью распознать рисунок. Используем исходное изображение.")
