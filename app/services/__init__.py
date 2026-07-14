"""Сервисы приложения."""

from app.services.ai_service import AIService
from app.services.history_service import HistoryService
from app.services.image_service import ImageService

try:
    from app.services.geometry_service import GeometryService
except ImportError:
    GeometryService = None

__all__ = ["AIService", "GeometryService", "HistoryService", "ImageService"]
