"""Утилиты для работы с файлами."""

from pathlib import Path


def ensure_directory_exists(directory: Path) -> bool:
    """Убедиться, что директория существует."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def get_file_extension(file_path: str) -> str:
    """Получить расширение файла."""
    return Path(file_path).suffix[1:].lower()


def get_file_name(file_path: str) -> str:
    """Получить имя файла."""
    return Path(file_path).name
