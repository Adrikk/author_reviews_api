from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from dependencies import Session
from exceptions import AppExceptions, AuthorDoesNotExist, BooksNotFoundError
from models import BooksDB
from schemas import BookCreate, BookPatch, BookPut


def get_all_books(db: Session) -> Sequence[BooksDB]:
    return db.scalars(select(BooksDB)).all()


def get_book_by_id(book_id: int, db: Session) -> BooksDB | None:
    return db.scalar(select(BooksDB).filter(BooksDB.id == book_id))


def create_book(db: Session, book_data: BookCreate) -> BooksDB:
    new_book = BooksDB(**book_data.model_dump())
    db.add(new_book)
    try:
        db.commit()
        db.refresh(new_book)
        return new_book
    except IntegrityError:
        db.rollback()
        raise AuthorDoesNotExist(
            "Книга не может быть добавлена, т.к. неправильно указан ID автора"
        )


def put_book(db: Session, book_data: BookPut, book_id: int) -> BooksDB:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        raise BooksNotFoundError("Книга не найдена")
    for field, data in book_data.model_dump().items():
        setattr(db_book, field, data)
    try:
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise AppExceptions("Возникла проблема при добавлении книги", 400)


def patch_book(db: Session, book_data: BookPatch, book_id: int) -> BooksDB:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        raise BooksNotFoundError("Книга не найдена")
    for field, data in book_data.model_dump(exclude_unset=True).items():
        setattr(db_book, field, data)
    try:
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise AppExceptions("Возникла проблема при добавлении книги", 400)


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        raise BooksNotFoundError("Книга не найдена")
    db.delete(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise AppExceptions("Не удалось удалить книгу. Попробуйте ещё раз", 400)
