"""Сервис для работы с изображениями."""

import base64
import sys
from pathlib import Path
from typing import Optional

from PIL import Image, UnidentifiedImageError
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from app.constants import SUPPORTED_IMAGE_FORMATS


class ImageService:
    """Сервис для работы с изображениями задач."""

    MAX_IMAGE_SIZE_MB = 10
    MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

    def validate_image(self, image_path: str) -> tuple[bool, str]:
        """Проверить корректность изображения.
        
        Returns:
            (is_valid, message): кортеж с результатом и сообщением об ошибке
        """
        try:
            path = Path(image_path)

            if not path.exists():
                return False, "Файл не найден."

            if not path.is_file():
                return False, "Это не файл."

            # Проверка расширения
            ext = path.suffix[1:].lower()
            if not ext or ext not in SUPPORTED_IMAGE_FORMATS:
                return False, "Поддерживаются только PNG, JPG, JPEG и WEBP."

            # Проверка размера
            file_size_bytes = path.stat().st_size
            if file_size_bytes > self.MAX_IMAGE_SIZE_BYTES:
                return False, "Размер изображения не должен превышать 10 МБ."

            # Проверка через Pillow
            try:
                with Image.open(path) as img:
                    img.verify()
            except UnidentifiedImageError:
                return False, "Файл повреждён или не является изображением."
            except Exception as exc:
                print(str(exc), file=sys.stderr)
                return False, "Файл повреждён или не является изображением."

            return True, ""

        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return False, "Ошибка при проверке изображения."

    def load_preview(
        self, image_path: str, max_width: int = 320, max_height: int = 220
    ) -> QPixmap:
        """Создать миниатюру изображения с сохранением пропорций.
        
        Args:
            image_path: путь к файлу
            max_width: максимальная ширина
            max_height: максимальная высота
            
        Returns:
            QPixmap с миниатюрой или пустой QPixmap при ошибке
        """
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                return QPixmap()

            scaled = pixmap.scaledToWidth(
                max_width,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            if scaled.height() > max_height:
                scaled = scaled.scaledToHeight(
                    max_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            return scaled

        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return QPixmap()

    def encode_image_to_base64(self, image_path: str) -> str:
        """Кодировать изображение в Base64.
        
        Args:
            image_path: путь к файлу
            
        Returns:
            строка Base64 без переносов
            
        Raises:
            Exception: если файл не найден или нечитаем
        """
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            return base64.b64encode(image_data).decode("utf-8")
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise

    def get_image_mime_type(self, image_path: str) -> str:
        """Получить MIME-тип изображения.
        
        Args:
            image_path: путь к файлу
            
        Returns:
            MIME-тип (image/png, image/jpeg, image/webp)
        """
        try:
            path = Path(image_path)
            ext = path.suffix[1:].lower()

            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "webp": "image/webp",
            }

            return mime_types.get(ext, "image/jpeg")

        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return "image/jpeg"

    def prepare_image_for_api(self, image_path: str) -> str:
        """Подготовить изображение для API в формате Data URL.
        
        Args:
            image_path: путь к файлу
            
        Returns:
            Data URL в формате data:image/type;base64,<данные>
        """
        try:
            mime_type = self.get_image_mime_type(image_path)
            base64_data = self.encode_image_to_base64(image_path)
            return f"data:{mime_type};base64,{base64_data}"
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise

    def get_file_info(self, image_path: str) -> dict:
        """Получить информацию о файле.
        
        Returns:
            словарь с именем файла, размером в МБ и расширением
        """
        try:
            path = Path(image_path)
            size_bytes = path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)

            return {
                "name": path.name,
                "size_bytes": size_bytes,
                "size_mb": f"{size_mb:.2f}",
                "extension": path.suffix[1:].lower(),
            }
        except Exception:
            return {"name": "Неизвестно", "size_mb": "0", "extension": ""}

    @staticmethod
    def get_image_dimensions(file_path: str) -> Optional[tuple[int, int]]:
        """Получить размеры изображения."""
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception:
            return None

    @staticmethod
    def get_image_format(file_path: str) -> Optional[str]:
        """Получить формат изображения."""
        try:
            with Image.open(file_path) as img:
                return img.format
        except Exception:
            return None

