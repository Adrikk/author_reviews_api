from fastapi import status


class AppExceptions(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class EntityNotFoundError(AppExceptions):
    """Базовая ошибка при не нахождении данных"""

    status_code = status.HTTP_404_NOT_FOUND


class EntityConflictError(AppExceptions):
    """Базовая ошибка при конфликтах (дубли username, email, ограничения при удалении)"""

    status_code = status.HTTP_409_CONFLICT


class AuthorAlreadyExistsError(EntityConflictError):
    """Выбрасывается при попытке создать автора с занятым username или email"""


class AuthorDoesNotExist(EntityNotFoundError):
    """Выбрасывается, если при попытке взаимодействия с каким-то автором не удается его найти по ID"""


class ViolationConstraintError(EntityConflictError):
    """Выбрасывается при попытке удаления записей на которые есть ссылки в других таблицах"""
