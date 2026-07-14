import sys

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_setup_ui_connections(qapp):
    from app.config import AppConfig
    from app.controllers import SolverController
    from app.ui.main_window import MainWindow
    from main import setup_ui_connections

    window = MainWindow()
    config = AppConfig()
    controller = SolverController(config=config)

    setup_ui_connections(window, controller, config)