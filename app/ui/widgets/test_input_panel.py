import pytest
from PySide6.QtWidgets import QApplication
from app.ui.widgets.input_panel import InputPanel

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

def test_input_panel_public_api(qapp):
    panel = InputPanel()
    required_attributes = [
        "solve_button",
        "clear_button",
        "photo_button",
        "document_button",
        "task_input",
        "subject_combo",
        "image_preview",
    ]

    for attr in required_attributes:
        assert hasattr(panel, attr), f"InputPanel missing attribute: {attr}"

    assert hasattr(panel.image_preview, "delete_image_button"), "image_preview missing delete_image_button"

    # If document_preview is used in main.py, add checks here
    if hasattr(panel, "document_preview"):
        assert hasattr(panel, "document_preview")
        assert hasattr(panel.document_preview, "delete_document_button")