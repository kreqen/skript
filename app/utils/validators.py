"""Валидаторы для проверки входных данных."""

from pathlib import Path


def validate_task_text(text: str) -> bool:
    """Проверить, что текст задачи не пуст."""
    return bool(text.strip())


def validate_subject(subject: str, valid_subjects: list[str]) -> bool:
    """Проверить, что выбранный предмет валидный."""
    return subject in valid_subjects


def validate_task_with_optional_image(text: str, image_path: str | None) -> bool:
    """Проверить, что задача имеет текст или изображение (или оба).
    
    Args:
        text: текст условия задачи
        image_path: путь к файлу изображения (может быть None)
        
    Returns:
        True, если есть текст или существует файл изображения
    """
    has_text = bool(text.strip())
    has_image = bool(image_path) and Path(image_path).exists()
    return has_text or has_image

