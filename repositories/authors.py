from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from dependencies import Session
from exceptions import (
    AuthorAlreadyExistsError,
    AuthorDoesNotExist,
    ViolationConstraintError,
)
from models import AuthorsDB
from schemas import AuthorCreate, AuthorPatch, AuthorPut


# Получить всех авторов
def get_all_authors(db: Session) -> Sequence[AuthorsDB]:
    return db.scalars(select(AuthorsDB)).all()


# Получить автора по ID
def get_author_by_id(author_id: int, db: Session) -> AuthorsDB | None:
    return db.scalar(select(AuthorsDB).filter(AuthorsDB.id == author_id))


# Создать нового автора в БД
def create_author(db: Session, author_data: AuthorCreate) -> AuthorsDB | None:
    new_author = AuthorsDB(**author_data.model_dump())
    db.add(new_author)
    try:
        db.commit()
        db.refresh(new_author)
        return new_author
    except IntegrityError as e:
        db.rollback()
        raise AuthorAlreadyExistsError(
            f"Автор с username='{new_author.username}' уже существует"
        ) from e


def put_author(db: Session, author_data: AuthorPut, author_id: int) -> AuthorsDB:
    db_author = db.scalar(select(AuthorsDB).filter(AuthorsDB.id == author_id))
    if not db_author:
        raise AuthorDoesNotExist("Автор с таким ID не найден.")
    for field, data in author_data.model_dump().items():
        setattr(db_author, field, data)
    try:
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError as e:
        db.rollback()
        raise AuthorAlreadyExistsError(
            "Автор с таким username или email уже существует"
        ) from e


def patch_author(db: Session, author_data: AuthorPatch, author_id: int) -> AuthorsDB:
    db_author = db.scalar(select(AuthorsDB).filter(AuthorsDB.id == author_id))
    if not db_author:
        raise AuthorDoesNotExist("Автор с таким ID не найден.")
    for field, data in author_data.model_dump(exclude_unset=True).items():
        setattr(db_author, field, data)
    try:
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError as e:
        db.rollback()
        raise AuthorAlreadyExistsError(
            "Автор с таким username или email уже существует"
        ) from e


def delete_author(db: Session, author_id: int) -> bool | None:
    db_author = db.scalar(select(AuthorsDB).filter(AuthorsDB.id == author_id))
    if not db_author:
        raise AuthorDoesNotExist("Автор не найден")
    try:
        db.delete(db_author)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        raise ViolationConstraintError(
            "Не удалось удалить автора, на его ID ссылаются в других таблицах."
        ) from e
