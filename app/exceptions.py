"""Пользовательские исключения для приложения."""

class SolverError(Exception):
    """Базовое исключение для ошибок решения задач."""
    pass


class VisionServiceError(SolverError):
    """Ошибка анализа геометрического изображения."""
    pass


class DocumentServiceError(SolverError):
    """Ошибка обработки документа."""
    pass

class MissingAPIKeyError(SolverError):
    """Ошибка отсутствия API-ключа."""
    pass


class AIConnectionError(SolverError):
    """Ошибка подключения к OpenAI."""
    pass


class AIResponseFormatError(SolverError):
    """Ошибка формата ответа от ИИ."""
    pass
