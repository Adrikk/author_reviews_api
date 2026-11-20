from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Модель автора
class Author(BaseModel):
    lastname: str = Field(..., min_length=3, max_length=20)
    firstname: str = Field(..., min_length=3, max_length=20)
    email: EmailStr = Field(max_length=30)
    username: str = Field(..., min_length=6, max_length=20)

    model_config = ConfigDict(extra="forbid")


# Модель при создании автора
class AuthorCreate(Author):
    password: str = Field(..., min_length=8, max_length=20)


# Модель для ответа по авторам
class AuthorResp(Author):
    id: int
    created: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthorPatch(BaseModel):
    lastname: str | None = Field(default=None, min_length=3, max_length=20)
    firstname: str | None = Field(default=None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default=None, max_length=30)
    username: str | None = Field(default=None, min_length=6, max_length=20)
    password: str | None = Field(default=None, min_length=8, max_length=20)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_patch(self):
        if not self.model_fields_set:
            raise ValueError("Нужно указать хотя бы одно поле для изменения")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Поля автора не могут быть null")
        return self


class AuthorCreateDB(Author):
    password_hash: str


# Книги
class Book(BaseModel):
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    is_shown: bool = False

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


class BookPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    description: str | None = Field(default=None, min_length=5)
    is_shown: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_patch(self):
        if not self.model_fields_set:
            raise ValueError("Нужно указать хотя бы одно поле для изменения")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Поля книги не могут быть null")
        return self


class Review(BaseModel):
    description: str = Field(..., min_length=3)
    rating: int = Field(..., ge=1, le=5)
    is_shown: bool = True

    model_config = ConfigDict(extra="forbid")


class ReviewCreate(Review):
    """
    Docstring for ReviewCreate
    """


class ReviewPatch(BaseModel):
    description: str | None = Field(default=None, min_length=3)
    rating: int | None = Field(default=None, ge=1, le=5)
    is_shown: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_patch(self):
        if not self.model_fields_set:
            raise ValueError("Нужно указать хотя бы одно поле для изменения")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Поля отзыва не могут быть null")
        return self


class ReviewResp(Review):
    id: int
    created: datetime
    author_id: int = Field(..., ge=1)
    book_id: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)
