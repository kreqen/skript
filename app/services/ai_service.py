"""Сервис для работы с искусственным интеллектом."""

import sys
from pathlib import Path
from typing import Tuple

from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    OpenAI,
    PermissionDeniedError,
    RateLimitError,
)

from app.config import AppConfig
from app.constants import SCHOOL_SOLVER_SYSTEM_PROMPT
from app.exceptions import (
    AIConnectionError,
    AIResponseFormatError,
    MissingAPIKeyError,
    SolverError,
)
from app.models import Solution, Task
from app.prompts.manager import PromptManager
from app.services.image_service import ImageService
from app.services.vision_service import VisionService
from app.utils import parse_openai_json_response


class AIService:
    """Сервис для решения задач через ИИ."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.image_service = ImageService()
        self.vision_service = VisionService(config)
        self.prompt_manager = PromptManager()

    def solve_task(self, task: Task) -> Solution:
        """Решить задачу в зависимости от режима."""
        mode = self.config.get_api_mode()

        # Если есть изображение и предмет Геометрия, сначала анализируем рисунок
        geometry_data = None
        if task.has_image() and task.subject.lower() == "геометрия":
            try:
                geometry_data = self.vision_service.analyze_image(task.image_path, task.subject)
            except Exception:
                # Логируем, но не прерываем решение
                geometry_data = None

        if mode == "test":
            solution = self.solve_in_test_mode(task)
            if geometry_data:
                solution.geometry_data = geometry_data
            return solution

        if mode == "openai":
            api_key = self.config.get_api_key()
            if not api_key:
                raise MissingAPIKeyError(
                    "API-ключ OpenAI не задан. Установите его в настройках."
                )
            # Формируем пользовательский промпт с учетом geometry_data
            user_prompt = self.prompt_manager.build_user_prompt(task)
            system_instructions = self.prompt_manager.compose_system_instructions(
                task, self.config.is_detailed_solution_enabled()
            )
            # Добавляем geometry_data в запрос (например, в instructions или input)
            # TODO: Реализовать передачу geometry_data в OpenAI запрос
            # Для примера просто вызываем solve_with_openai без изменений
            solution = self.solve_with_openai(task)
            if geometry_data:
                solution.geometry_data = geometry_data
            return solution

        raise SolverError("Неизвестный режим работы. Проверьте настройки приложения.")

    def solve_in_test_mode(self, task: Task) -> Solution:
        """Вернуть демонстрационное тестовое решение."""
        short_answer = "Это тестовый ответ новой версии приложения."
        has_image = task.has_image()

        steps = [
            "Получено условие задачи.",
            "Проверена корректность введённых данных.",
            "Определён выбранный школьный предмет.",
        ]

        if has_image:
            steps.append("Изображение задачи успешно загружено и проверено.")
            steps.append("В режиме OpenAI API оно будет проанализировано искусственным интеллектом.")
        else:
            steps.append("Подготовлена структура для подключения искусственного интеллекта.")

        formulas = ["В тестовой версии формулы пока не используются."]
        explanation = (
            "После подключения ИИ здесь появится подробное объяснение решения."
        )
        verification = "Ответ проверен на соответствие условия задачи."

        # Добавляем демонстрационные данные geometry_data в тестовом режиме
        geometry_data = None
        if has_image and task.subject.lower() == "геометрия":
            geometry_data = {
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

        source = self._determine_source(task)
        solution = Solution(
            subject=task.subject,
            short_answer=short_answer,
            steps=steps,
            formulas=formulas,
            explanation=explanation,
            verification=verification,
            source=source,
        )
        if geometry_data:
            solution.geometry_data = geometry_data
        return solution

    def solve_with_openai(self, task: Task) -> Solution:
        """Запросить решение у OpenAI Responses API с поддержкой изображений."""
        api_key = self.config.get_api_key()
        if not api_key:
            raise MissingAPIKeyError(
                "API-ключ OpenAI не задан. Установите его в настройках."
            )

        model_name = self.config.get_model()
        
        # Проверить, что есть либо текст, либо изображение
        if not task.text.strip() and not task.has_image():
            raise SolverError(
                "Введите условие задачи или загрузите фотографию."
            )
        
        # Проверить длину текста, если он есть
        if task.text.strip():
            self._validate_task_text(task.text)

        user_prompt = self.prompt_manager.build_user_prompt(task)
        system_instructions = self.prompt_manager.compose_system_instructions(
            task, self.config.is_detailed_solution_enabled()
        )

        try:
            client = OpenAI(api_key=api_key)

            # Построить Input в зависимости от наличия изображения
            if task.has_image():
                input_data = self._build_multimodal_input(user_prompt, task.image_path)
            else:
                input_data = user_prompt

            response = client.responses.create(
                model=model_name,
                instructions=system_instructions,
                input=input_data,
                timeout=60,
            )

            output_text = getattr(response, "output_text", None)
            if not isinstance(output_text, str):
                raise AIResponseFormatError(
                    "ИИ вернул ответ в неправильном формате. Попробуйте ещё раз."
                )

            parsed = parse_openai_json_response(output_text)
            source = self._determine_source(task)

            return Solution(
                subject=parsed["detected_subject"] or task.subject,
                detected_subject=parsed["detected_subject"],
                short_answer=parsed["short_answer"],
                steps=parsed["steps"],
                formulas=parsed["formulas"],
                explanation=parsed["explanation"],
                verification=parsed["verification"],
                source=source,
            )
        except MissingAPIKeyError:
            raise
        except AIResponseFormatError:
            raise
        except AuthenticationError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Неверный API-ключ. Проверьте ключ в настройках."
            ) from exc
        except PermissionDeniedError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "У API-ключа недостаточно прав для выполнения запроса."
            ) from exc
        except RateLimitError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Превышен лимит API или закончились средства на API-балансе."
            ) from exc
        except APITimeoutError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "OpenAI не ответил вовремя. Попробуйте ещё раз."
            ) from exc
        except APIConnectionError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Не удалось подключиться к OpenAI. Проверьте интернет."
            ) from exc
        except BadRequestError as exc:
            print(str(exc), file=sys.stderr)
            # Проверка на ошибку неподдерживаемой модели для изображений
            if "vision" in str(exc).lower() or "image" in str(exc).lower():
                raise AIConnectionError(
                    "Выбранная модель не поддерживает анализ изображений. Измените модель в настройках."
                ) from exc
            raise AIConnectionError(
                "OpenAI не смог обработать запрос. Проверьте условие задачи."
            ) from exc
        except InternalServerError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "На стороне OpenAI произошла временная ошибка."
            ) from exc
        except APIStatusError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "OpenAI вернул ошибку при выполнении запроса."
            ) from exc
        except APIError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Произошла ошибка при обращении к ИИ."
            ) from exc
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Не удалось получить ответ от OpenAI. Попробуйте ещё раз."
            ) from exc

    def test_connection(self) -> Tuple[bool, str]:
        """Проверить подключение к OpenAI."""
        api_key = self.config.get_api_key()
        if not api_key:
            raise MissingAPIKeyError(
                "API-ключ OpenAI не задан. Установите его в настройках."
            )

        model_name = self.config.get_model()
        try:
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=model_name,
                instructions=SCHOOL_SOLVER_SYSTEM_PROMPT,
                input="Ответь одним словом: OK",
                timeout=60,
            )
            output_text = getattr(response, "output_text", "")
            if "ok" in output_text.lower():
                return True, "Подключение работает"
            return False, "Подключение установлено, но ответ не подтверждён"
        except MissingAPIKeyError:
            raise
        except AuthenticationError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Неверный API-ключ. Проверьте ключ в настройках."
            ) from exc
        except PermissionDeniedError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "У API-ключа недостаточно прав для выполнения запроса."
            ) from exc
        except RateLimitError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Превышен лимит API или закончились средства на API-балансе."
            ) from exc
        except APITimeoutError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "OpenAI не ответил вовремя. Попробуйте ещё раз."
            ) from exc
        except APIConnectionError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Не удалось подключиться к OpenAI. Проверьте интернет."
            ) from exc
        except BadRequestError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "OpenAI не смог обработать запрос. Проверьте условие задачи."
            ) from exc
        except InternalServerError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "На стороне OpenAI произошла временная ошибка."
            ) from exc
        except APIStatusError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "OpenAI вернул ошибку при выполнении запроса."
            ) from exc
        except APIError as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Произошла ошибка при обращении к ИИ."
            ) from exc
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            raise AIConnectionError(
                "Не удалось проверить подключение. Попробуйте позже."
            ) from exc

    def _build_user_prompt(self, task: Task) -> str:
        """Сформировать пользовательский запрос для модели.
        
        Включает информацию об изображении, если оно присутствует.
        """
        detailed = "да" if self.config.is_detailed_solution_enabled() else "нет"

        prompt_parts = [
            f"Выбранный предмет: {task.subject}\n"
            f"Подробное решение: {detailed}\n"
        ]

        # Информация об изображении
        if task.has_image():
            prompt_parts.append("К задаче приложено изображение. Прочитай условие с изображения.")

        # Текст задачи
        prompt_parts.append("\nУсловие задачи:")
        if task.text.strip():
            prompt_parts.append(f"{task.text.strip()}")
        else:
            prompt_parts.append("(см. изображение)")

        # Комментарий пользователя
        if task.has_image():
            if task.text.strip():
                prompt_parts.append(f"\nКомментарий пользователя:\n{task.text.strip()}")
            else:
                prompt_parts.append("\nКомментарий пользователя отсутствует.")

        return "\n".join(prompt_parts)

    def _build_multimodal_input(self, text_prompt: str, image_path: str | None) -> list:
        """Построить мультимодальный ввод для Responses API.
        
        Args:
            text_prompt: текстовый запрос
            image_path: путь к изображению
            
        Returns:
            список с сообщением, содержащим текст и изображение (если есть)
        """
        content = [
            {
                "type": "input_text",
                "text": text_prompt,
            }
        ]

        # Добавить изображение, если оно существует
        if image_path and Path(image_path).exists():
            try:
                image_data_url = self.image_service.prepare_image_for_api(image_path)
                content.append(
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                    }
                )
            except Exception as exc:
                print(f"Ошибка при подготовке изображения: {exc}", file=sys.stderr)
                # Продолжить с текстом, даже если изображение не удалось подготовить

        return [
            {
                "role": "user",
                "content": content,
            }
        ]

    def _determine_source(self, task: Task) -> str:
        """Определить источник задачи для результата."""
        has_text = bool(task.text.strip())
        has_image = task.has_image()

        if has_text and has_image:
            return "Текст и изображение"
        if has_image:
            return "Изображение"
        return "Текст"

    def _validate_task_text(self, text: str) -> None:
        """Проверить длину текста задачи."""
        if len(text) > 15000:
            raise SolverError(
                "Текст задачи слишком длинный. Ограничение 15000 символов."
            )
