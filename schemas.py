from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Модель автора
class Author(BaseModel):
    lastname: str = Field(..., min_length=3, max_length=20)
    firstname: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(max_length=30)
    username: str = Field(..., min_length=6, max_length=20)

    model_config = ConfigDict(extra="forbid")


# Модель при создании автора
class AuthorCreate(Author):
    pass


# Модель для ответа по авторам
class AuthorResp(Author):
    id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)


# Модель для put запроса по автору
class AuthorPut(Author):
    pass


class AuthorPatch(BaseModel):
    lastname: str | None = None
    firstname: str | None = None
    email: EmailStr | None = None
    username: str | None = None


# Книги
class Book(BaseModel):
    author_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    is_shown: bool | None = False

    model_config = ConfigDict(extra="forbid")


# Модель валидации при создании
class BookCreate(Book):
    pass


# Модель ответа созданной книги
class BookResp(Book):
    id: int
    created: datetime
    rating: float

    model_config = ConfigDict(from_attributes=True)


class BookPut(Book):
    pass


class BookPatch(BaseModel):
    name: str | None = Field(..., min_length=3)
    description: str | None = Field(..., min_length=5)
    is_shown: bool | None = False


class Review(BaseModel):
    author_id: int = Field(..., ge=1)
    book_id: int = Field(..., ge=1)
    description: str = Field(..., min_length=3)
    rating: int = Field(..., ge=1, le=5)
    is_shown: bool | None = True

    model_config = ConfigDict(extra="forbid")


class ReviewCreate(Review):
    pass


class ReviewPatch(Review):
    id: int = Field(..., ge=1)


class ReviewResp(Review):
    id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)
