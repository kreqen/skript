"""Контроллер для управления решением задач."""

from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from pathlib import Path
from typing import Optional

from app.config import AppConfig
from app.models import Task, Solution
from app.services import AIService, HistoryService, ImageService
from app.utils import validate_task_text, validate_subject
from app.constants import SUBJECTS
from app.exceptions import SolverError


class SolveTaskSignals(QObject):
    """Сигналы рабочего потока решения задачи."""

    solved = Signal(object)
    error = Signal(str)


class SolveTaskWorker(QRunnable):
    """Рабочий поток для решения задач без блокировки UI."""

    def __init__(
        self, task: Task, ai_service: AIService, parent: Optional[QObject] = None
    ) -> None:
        """Инициализировать рабочий поток."""
        super().__init__()
        self.task = task
        self.ai_service = ai_service
        self.signals = SolveTaskSignals(parent)

    def run(self) -> None:
        """Выполнить решение задачи в отдельном потоке."""
        try:
            solution = self.ai_service.solve_task(self.task)
            self.signals.solved.emit(solution)
        except SolverError as error:
            self.signals.error.emit(str(error))
        except Exception as error:
            self.signals.error.emit("Ошибка при решении задачи. Попробуйте ещё раз.")


class SolverController(QObject):
    """Контроллер для управления логикой решения задач."""

    task_solved = Signal(object)
    task_error = Signal(str)
    solving_started = Signal()
    solving_finished = Signal()

    def __init__(self, config: AppConfig) -> None:
        """Инициализировать контроллер."""
        super().__init__()
        self.config = config
        self.ai_service = AIService(config)
        self.history_service = HistoryService()
        self.image_service = ImageService()
        self.thread_pool = QThreadPool()

    def solve_task(
        self, subject: str, task_text: str, image_path: Optional[str] = None
    ) -> bool:
        """Решить задачу в отдельном потоке."""
        if not self._validate_input(subject, task_text, image_path):
            return False

        task = Task(subject=subject, text=task_text, image_path=image_path)

        # Показать сообщение о начале анализа, если геометрия с изображением
        if task.has_image() and task.subject.lower() == "геометрия":
            self.analysis_started()

        worker = SolveTaskWorker(task, self.ai_service)
        worker.signals.solved.connect(self._on_task_solved)
        worker.signals.error.connect(self._on_task_error)

        self.solving_started.emit()
        self.thread_pool.start(worker)

        return True

    def analysis_started(self):
        # TODO: Реализовать сигнал или callback для UI о начале анализа изображения
        pass

    def analysis_finished(self, success: bool):
        # TODO: Реализовать сигнал или callback для UI о завершении анализа изображения
        pass

    def _validate_input(
        self, subject: str, task_text: str, image_path: Optional[str] = None, document_path: Optional[str] = None
    ) -> bool:
        """Проверить входные данные."""
        # Проверить, что есть либо текст, либо изображение, либо документ
        has_text = validate_task_text(task_text)
        has_valid_image = image_path and Path(image_path).exists()
        has_valid_document = document_path and Path(document_path).exists()

        if not has_text and not has_valid_image and not has_valid_document:
            self.task_error.emit("Введите условие, загрузите фотографию или выберите документ.")
            return False

        if not validate_subject(subject, SUBJECTS):
            self.task_error.emit("Выбранный предмет не валидный.")
            return False

        return True

    def _on_task_solved(self, solution: Solution) -> None:
        """Обработать успешное решение задачи."""
        self.task_solved.emit(solution)
        self.solving_finished.emit()

        # Автоматически построить геометрический рисунок, если есть данные
        geometry_data = getattr(solution, "geometry_data", None)
        if geometry_data:
            # Предполагается, что UI подписан на сигнал task_solved и обновит рисунок
            pass

    def _on_task_error(self, error: str) -> None:
        """Обработать ошибку при решении задачи."""
        self.task_error.emit(error)
        self.solving_finished.emit()

    def save_to_history(
        self,
        subject: str,
        task_text: str,
        short_answer: str,
        full_solution: str,
        image_path: Optional[str] = None,
    ) -> bool:
        """Сохранить решение в историю."""
        return self.history_service.add_solution(
            subject, task_text, short_answer, full_solution, image_path
        )

    def get_history(self) -> list[dict]:
        """Получить историю решений."""
        return self.history_service.load_history()

    def clear_history(self) -> bool:
        """Очистить историю решений."""
        return self.history_service.clear_history()
