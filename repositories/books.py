from collections.abc import Sequence

from sqlalchemy import select

from dependencies import Session
from models import BooksDB
from schemas import AuthorCreate, AuthorPut


# Получить всех авторов
def get_all_books(db: Session) -> Sequence[BooksDB]:
    return db.scalars(select(BooksDB)).all()


# Получить автора по ID
def get_book_by_id(book_id: int, db: Session) -> BooksDB | None:
    return db.scalar(select(BooksDB).filter(BooksDB.id == book_id))


# Создать нового автора в БД
def create_book(db: Session, book_data: AuthorCreate) -> BooksDB:
    new_book = BooksDB(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def put_book(db: Session, book_data: AuthorPut, book_id: int) -> BooksDB | None:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        return None
    for field, data in book_data.model_dump().items():
        setattr(db_book, field, data)
    db.commit()
    db.refresh(db_book)
    return db_book


def patch_book(db: Session, book_data: AuthorPut, book_id: int) -> BooksDB | None:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        return None
    for field, data in book_data.model_dump(exclude_unset=True).items():
        setattr(db_book, field, data)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not db_book:
        return
    db.delete(db_book)
    db.commit()
