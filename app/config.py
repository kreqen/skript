"""Конфигурация приложения."""

from pathlib import Path
from typing import Any

from PySide6.QtCore import QSettings

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"

DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE_PATH = DATA_DIR / "history.json"
ENV_FILE = PROJECT_ROOT / ".env"

SETTINGS_ORGANIZATION = "School AI Solver"
SETTINGS_APPLICATION = "SchoolAISolver"

DEFAULT_API_MODE = "test"
DEFAULT_API_MODEL = "gpt-4.1-mini"
DEFAULT_DETAILED_SOLUTION = True
DEFAULT_AUTO_SAVE_HISTORY = True


class AppConfig:
    """Управление настройками приложения."""

    def __init__(self) -> None:
        self.settings = QSettings(SETTINGS_ORGANIZATION, SETTINGS_APPLICATION)

    def get_api_key(self) -> str:
        value = self.settings.value("api/openai_key", "", type=str)
        return value.strip() if isinstance(value, str) else ""

    def set_api_key(self, api_key: str) -> None:
        self.settings.setValue("api/openai_key", api_key.strip())
        self.settings.sync()

    def get_api_mode(self) -> str:
        value = self.settings.value("api/mode", DEFAULT_API_MODE, type=str)
        return value if value in {"test", "openai"} else DEFAULT_API_MODE

    def set_api_mode(self, mode: str) -> None:
        if mode not in {"test", "openai"}:
            mode = DEFAULT_API_MODE
        self.settings.setValue("api/mode", mode)
        self.settings.sync()

    def get_model(self) -> str:
        value = self.settings.value("api/model", DEFAULT_API_MODEL, type=str)
        return value.strip() if isinstance(value, str) and value.strip() else DEFAULT_API_MODEL

    def set_model(self, model_name: str) -> None:
        self.settings.setValue("api/model", model_name.strip())
        self.settings.sync()

    def is_detailed_solution_enabled(self) -> bool:
        return self.settings.value(
            "solver/detailed_solution", DEFAULT_DETAILED_SOLUTION, type=bool
        )

    def set_detailed_solution(self, enabled: bool) -> None:
        self.settings.setValue("solver/detailed_solution", enabled)
        self.settings.sync()

    def is_history_enabled(self) -> bool:
        return self.settings.value(
            "history/auto_save", DEFAULT_AUTO_SAVE_HISTORY, type=bool
        )

    def set_history_enabled(self, enabled: bool) -> None:
        self.settings.setValue("history/auto_save", enabled)
        self.settings.sync()
