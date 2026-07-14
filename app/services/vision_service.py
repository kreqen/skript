import json
import logging
from typing import Dict, Any

from app.config import AppConfig
from app.exceptions import VisionServiceError

logger = logging.getLogger(__name__)

class VisionService:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def analyze_image(self, image_path: str, subject: str) -> Dict[str, Any]:
        """
        Анализирует изображение геометрической задачи и возвращает структуру рисунка в JSON формате.

        Если включён тестовый режим, возвращает демонстрационный JSON.

        Args:
            image_path: путь к изображению
            subject: предмет задачи

        Returns:
            dict с распознанными данными рисунка
        """
        if self.config.get_api_mode() == "test":
            return self._demo_response()

        if subject.lower() != "геометрия":
            return {}

        # Формируем Vision Prompt для OpenAI
        vision_prompt = self._build_vision_prompt()

        # Здесь должен быть вызов OpenAI с vision_prompt и image_path
        # Для примера заглушка:
        try:
            # TODO: Реализовать вызов OpenAI с vision_prompt и обработку ответа
            # response_text = call_openai_api(vision_prompt, image_path)
            # vision_data = json.loads(response_text)
            vision_data = {}  # Заглушка
            self._log_vision_data(vision_data)
            return vision_data
        except Exception as e:
            logger.error(f"VisionService error: {e}")
            raise VisionServiceError("Ошибка при анализе изображения.")

    def _build_vision_prompt(self) -> str:
        prompt = (
            "Определи структуру геометрического рисунка на изображении. "
            "Верни строго JSON с полями: figure_type, points, segments, angles, circles, radii, heights, medians, bisectors, text. "
            "Не решай задачу, только определи структуру."
        )
        return prompt

    def _log_vision_data(self, data: Dict[str, Any]) -> None:
        if not logger.isEnabledFor(logging.DEBUG):
            return
        figure_type = data.get("figure_type", "неизвестно")
        points = data.get("points", [])
        segments = data.get("segments", {})
        angles = data.get("angles", {})
        logger.debug("===== Vision =====")
        logger.debug(f"Тип фигуры: {figure_type}")
        logger.debug(f"Количество точек: {len(points)}")
        logger.debug(f"Количество сторон: {len(segments)}")
        logger.debug(f"Количество углов: {len(angles)}")

    def _demo_response(self) -> Dict[str, Any]:
        return {
            "figure_type": "triangle",
            "points": ["A", "B", "C"],
            "segments": {
                "AB": 6,
                "BC": 8,
                "AC": 10
            },
            "angles": {
                "ABC": 90
            },
            "circles": [],
            "radii": [],
            "heights": [],
            "medians": [],
            "bisectors": [],
            "text": [
                "AB = 6",
                "BC = 8"
            ]
        }