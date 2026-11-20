from fastapi import status


class AppExceptions(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_message: str = "Ошибка приложения"

    def __init__(self, message: str | None = None, status_code: int | None = None):
        self.message = message or self.default_message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class ConflictError(AppExceptions):
    """Ошибка при конфликтах данных"""

    status_code = status.HTTP_409_CONFLICT


class DatabaseError(AppExceptions):
    """Ошибка при работе с базой"""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class InvalidCredentialsError(AppExceptions):
    """Ошибка при попытке авторизации"""

    status_code = status.HTTP_401_UNAUTHORIZED


class CredentialsError(InvalidCredentialsError):
    message = "Введены неправильные данные для авторизации"


class PermissionDeniedError(AppExceptions):
    message = "Доступ запрещен"
    status_code = status.HTTP_403_FORBIDDEN


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


class BooksNotFoundError(EntityNotFoundError):
    """Выбрасывается, если книга не была найдена"""


class ReviewsNotFoundError(EntityNotFoundError):
    """Выбрасывается, если отзыв не был найден"""
