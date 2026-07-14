"""Главная точка входа приложения School AI Solver."""

import sys
import traceback
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtWidgets import QApplication, QLineEdit, QMessageBox

from app.config import AppConfig
from app.controllers import SolverController
from app.exceptions import AIConnectionError, MissingAPIKeyError, SolverError
from app.ui import MainWindow
from app.ui.pages import SolverPage


class ConnectionWorkerSignals(QObject):
    finished = Signal(bool, str)
    error = Signal(str)


class ConnectionWorker(QRunnable):
    def __init__(self, controller: SolverController) -> None:
        super().__init__()
        self.controller = controller
        self.signals = ConnectionWorkerSignals()

    def run(self) -> None:
        try:
            success, message = self.controller.ai_service.test_connection()
            self.signals.finished.emit(success, message)
        except Exception as exc:
            self.signals.error.emit(str(exc))


def setup_exception_handler(app: QApplication) -> None:
    """Установить глобальный обработчик необработанных исключений."""

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.exit(0)

        error_msg = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )
        print(error_msg, file=sys.stderr)

        QMessageBox.critical(
            None,
            "Критическая ошибка",
            f"Произошла непредвиденная ошибка:\n\n{exc_value}",
        )

    sys.excepthook = handle_exception


def setup_ui_connections(
    window: MainWindow, controller: SolverController, config: AppConfig
) -> None:
    """Подключить сигналы и слоты для интерфейса."""
    solver_page = window.solver_page
    settings_page = window.settings_page

    solver_page.input_panel.solve_button.clicked.connect(
        lambda: on_solve_clicked(solver_page, controller, window)
    )
    solver_page.input_panel.clear_button.clicked.connect(
        lambda: on_clear_clicked(solver_page)
    )
    solver_page.input_panel.photo_button.clicked.connect(
        lambda: on_photo_clicked(solver_page)
    )
    solver_page.input_panel.image_preview.delete_image_button.clicked.connect(
        lambda: on_delete_image_clicked(solver_page)
    )
    solver_page.input_panel.image_preview.preview_area.mouseDoubleClickEvent = (
        lambda event: on_preview_double_clicked(solver_page, window)
    )
    
    solver_page.result_panel.copy_button.clicked.connect(
        lambda: on_copy_clicked(solver_page, window)
    )
    solver_page.result_panel.save_button.clicked.connect(
        lambda: on_save_clicked(solver_page, controller, window)
    )
    solver_page.result_panel.demo_figure_button.clicked.connect(
        lambda: on_demo_figure_clicked(solver_page)
    )

    controller.task_solved.connect(
        lambda solution: on_task_solved(
            solver_page, solution, window, controller, config
        )
    )
    controller.task_error.connect(
        lambda error: on_task_error(error, window)
    )
    controller.solving_started.connect(
        lambda: on_solving_started(solver_page)
    )
    controller.solving_finished.connect(
        lambda: on_solving_finished(solver_page)
    )

    window.history_page.clear_history_button.clicked.connect(
        lambda: on_clear_history(window, controller)
    )

    settings_page.toggle_key_visibility_button.clicked.connect(
        lambda: on_toggle_api_key_visibility(settings_page)
    )
    settings_page.check_connection_button.clicked.connect(
        lambda: on_check_connection(window, controller)
    )
    settings_page.save_settings_button.clicked.connect(
        lambda: on_save_settings(window, config)
    )

    load_settings_into_ui(settings_page, config)


def load_settings_into_ui(settings_page, config: AppConfig) -> None:
    """Загрузить настройки в интерфейс страницы настроек."""
    mode = config.get_api_mode()
    settings_page.api_mode_combo.setCurrentIndex(0 if mode == "test" else 1)
    settings_page.model_input.setText(config.get_model())
    settings_page.api_key_input.setText(config.get_api_key())
    settings_page.verbose_checkbox.setChecked(config.is_detailed_solution_enabled())
    settings_page.auto_save_checkbox.setChecked(config.is_history_enabled())
    settings_page.connection_status_label.setText("Статус подключения: не проверено")
    settings_page.toggle_key_visibility_button.setText("Показать ключ")
    settings_page.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)


def on_solve_clicked(
    solver_page: SolverPage, controller: SolverController, window: MainWindow
) -> None:
    """Обработать клик кнопки решить задачу."""
    subject = solver_page.input_panel.subject_input.currentText()
    task_text = solver_page.input_panel.task_input.toPlainText()
    image_path = solver_page.input_panel.image_preview.get_image_path()

    controller.solve_task(subject, task_text, image_path)


def on_clear_clicked(solver_page: SolverPage) -> None:
    """Обработать клик кнопки очистки."""
    solver_page.input_panel.task_input.clear()
    solver_page.result_panel.answer_output.clear()
    solver_page.input_panel.image_preview.clear_preview()


def on_photo_clicked(solver_page: SolverPage) -> None:
    """Обработать клик кнопки загрузить фото."""
    from PySide6.QtWidgets import QFileDialog
    from app.services import ImageService

    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Выберите файл с задачей",
        "",
        "Изображения (*.png *.jpg *.jpeg *.webp)",
    )

    if file_path:
        # Проверить изображение
        image_service = ImageService()
        is_valid, error_message = image_service.validate_image(file_path)

        if not is_valid:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(None, "Ошибка при загрузке фото", error_message)
            return

        # Установить изображение в предпросмотр
        solver_page.input_panel.image_preview.set_image(file_path)


def on_delete_image_clicked(solver_page: SolverPage) -> None:
    """Обработать клик кнопки удалить фото."""
    solver_page.input_panel.image_preview.clear_preview()


def on_preview_double_clicked(solver_page: SolverPage, window: MainWindow) -> None:
    """Обработать двойной клик по предпросмотру для открытия диалога."""
    from app.ui.widgets import ImagePreviewDialog

    image_path = solver_page.input_panel.image_preview.get_image_path()
    if image_path:
        dialog = ImagePreviewDialog(image_path, window)
        dialog.exec()

def on_copy_clicked(solver_page: SolverPage, window: MainWindow) -> None:
    """Обработать клик кнопки копировать."""
    from PySide6.QtGui import QClipboard, QGuiApplication

    answer_text = solver_page.result_panel.answer_output.toPlainText().strip()
    if answer_text:
        clipboard: QClipboard = QGuiApplication.clipboard()
        clipboard.setText(answer_text)
        window.status_bar.showMessage("Результат скопирован в буфер обмена")
    else:
        QMessageBox.warning(window, "Внимание", "Нет результата для копирования.")


def on_save_clicked(
    solver_page: SolverPage, controller: SolverController, window: MainWindow
) -> None:
    """Обработать клик кнопки сохранить."""
    subject = solver_page.input_panel.subject_input.currentText()
    task_text = solver_page.input_panel.task_input.toPlainText()
    answer_text = solver_page.result_panel.answer_output.toPlainText()

    if not answer_text:
        QMessageBox.warning(window, "Внимание", "Нет данных для сохранения.")
        return

    image_path = solver_page.input_panel.image_preview.get_image_path()

    success = controller.save_to_history(
        subject, task_text, "", answer_text, image_path
    )

    if success:
        window.history_page.load_history(controller.get_history())
        window.status_bar.showMessage("Решение сохранено в историю")
        QMessageBox.information(window, "Успешно", "Решение сохранено в историю.")
    else:
        QMessageBox.critical(window, "Ошибка", "Не удалось сохранить решение.")


def on_demo_figure_clicked(solver_page: SolverPage) -> None:
    """Обработать клик кнопки показать пример рисунка."""
    from PySide6.QtGui import QPixmap
    from app.services import GeometryService

    service = GeometryService()
    image_bytes = service.create_demo_figure()

    pixmap = QPixmap()
    pixmap.loadFromData(image_bytes)
    scaled_pixmap = pixmap.scaledToWidth(300)

    solver_page.result_panel.geometry_area.setPixmap(scaled_pixmap)


def on_task_solved(
    solver_page: SolverPage,
    solution,
    window: MainWindow,
    controller: SolverController,
    config: AppConfig,
) -> None:
    """Обработать успешное решение задачи."""
    solver_page.result_panel.answer_output.setPlainText(solution.format_as_text())

    if config.is_history_enabled():
        subject = solution.subject
        task_text = solver_page.input_panel.task_input.toPlainText()
        image_path = solver_page.input_panel.image_preview.get_image_path()
        success = controller.save_to_history(
            subject,
            task_text,
            solution.short_answer,
            solution.format_as_text(),
            image_path,
        )
        if not success:
            print("Не удалось автоматически сохранить решение в историю.", file=sys.stderr)
        else:
            window.history_page.load_history(controller.get_history())

    window.status_bar.showMessage("Решение готово")
    QMessageBox.information(window, "Готово", "Решение готово")


def on_task_error(error: str, window: MainWindow) -> None:
    """Обработать ошибку при решении задачи."""
    window.status_bar.showMessage("Ошибка при решении")
    QMessageBox.warning(window, "Ошибка", error)


def on_solving_started(solver_page: SolverPage) -> None:
    """Обработать начало решения задачи."""
    solver_page.input_panel.solve_button.setEnabled(False)
    solver_page.input_panel.solve_button.setText("Решаем…")
    solver_page.input_panel.clear_button.setEnabled(False)
    solver_page.input_panel.photo_button.setEnabled(False)


def on_solving_finished(solver_page: SolverPage) -> None:
    """Обработать завершение решения задачи."""
    solver_page.input_panel.solve_button.setEnabled(True)
    solver_page.input_panel.solve_button.setText("Решить задачу")
    solver_page.input_panel.clear_button.setEnabled(True)
    solver_page.input_panel.photo_button.setEnabled(True)


def on_clear_history(window: MainWindow, controller: SolverController) -> None:
    """Обработать очистку истории."""
    reply = QMessageBox.question(
        window,
        "Подтверждение",
        "Вы уверены, что хотите очистить всю историю?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )

    if reply == QMessageBox.StandardButton.Yes:
        if controller.clear_history():
            window.history_page.set_empty_message()
            window.status_bar.showMessage("История очищена")
            QMessageBox.information(window, "Успешно", "История очищена.")
        else:
            QMessageBox.critical(window, "Ошибка", "Не удалось очистить историю.")


def on_toggle_api_key_visibility(settings_page) -> None:
    """Показать или скрыть API-ключ в поле ввода."""
    if settings_page.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
        settings_page.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        settings_page.toggle_key_visibility_button.setText("Скрыть ключ")
    else:
        settings_page.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        settings_page.toggle_key_visibility_button.setText("Показать ключ")


def on_check_connection(window: MainWindow, controller: SolverController) -> None:
    """Проверить подключение к OpenAI."""
    settings_page = window.settings_page
    if settings_page.api_mode_combo.currentText() != "OpenAI API":
        QMessageBox.warning(
            window,
            "Внимание",
            "Проверка доступна только в режиме OpenAI API.",
        )
        return

    settings_page.check_connection_button.setEnabled(False)
    settings_page.check_connection_button.setText("Проверяем…")
    settings_page.connection_status_label.setText("Статус подключения: проверка...")

    worker = ConnectionWorker(controller)
    worker.signals.finished.connect(
        lambda ok, msg: on_connection_result(window, settings_page, ok, msg)
    )
    worker.signals.error.connect(
        lambda msg: on_connection_error(window, settings_page, msg)
    )
    controller.thread_pool.start(worker)


def on_connection_result(
    window: MainWindow,
    settings_page,
    success: bool,
    message: str,
) -> None:
    """Обработать результат проверки подключения."""
    settings_page.check_connection_button.setEnabled(True)
    settings_page.check_connection_button.setText("Проверить подключение")
    settings_page.connection_status_label.setText(f"Статус подключения: {message}")

    if success:
        QMessageBox.information(window, "Успех", message)
    else:
        QMessageBox.warning(window, "Внимание", message)


def on_connection_error(window: MainWindow, settings_page, message: str) -> None:
    """Обработать ошибку проверки подключения."""
    settings_page.check_connection_button.setEnabled(True)
    settings_page.check_connection_button.setText("Проверить подключение")
    settings_page.connection_status_label.setText(f"Статус подключения: {message}")
    QMessageBox.warning(window, "Ошибка подключения", message)


def on_save_settings(window: MainWindow, config: AppConfig) -> None:
    """Обработать сохранение настроек."""
    settings_page = window.settings_page
    api_key = settings_page.api_key_input.text().strip()
    mode = (
        "test"
        if settings_page.api_mode_combo.currentText() == "Тестовый режим"
        else "openai"
    )
    model_name = settings_page.model_input.text().strip() or config.get_model()

    config.set_api_key(api_key)
    config.set_api_mode(mode)
    config.set_model(model_name)
    config.set_detailed_solution(settings_page.verbose_checkbox.isChecked())
    config.set_history_enabled(settings_page.auto_save_checkbox.isChecked())

    api_key = ""

    settings_page.connection_status_label.setText("Статус подключения: не проверено")
    window.status_bar.showMessage("Настройки сохранены")
    QMessageBox.information(window, "Успешно", "Настройки сохранены.")


def main() -> None:
    """Главная функция приложения."""
    app = QApplication(sys.argv)
    app.setApplicationName("School AI Solver")
    app.setApplicationVersion("1.0.0")

    setup_exception_handler(app)

    config = AppConfig()
    window = MainWindow()
    controller = SolverController(config)

    setup_ui_connections(window, controller, config)
    window.history_page.load_history(controller.get_history())

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
