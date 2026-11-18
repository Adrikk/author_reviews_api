from collections.abc import Sequence

from sqlalchemy import select

from dependencies import Session
from models import BooksDB
from schemas import BookCreate, BookPatch


def get_all(db: Session) -> Sequence[BooksDB]:
    return db.scalars(select(BooksDB)).all()


def get_by_id(db: Session, book_id: int) -> BooksDB | None:
    return db.scalar(select(BooksDB).where(BooksDB.id == book_id))


def create(db: Session, book_data: BookCreate) -> BooksDB:
    new_book = BooksDB(**book_data.model_dump())
    db.add(new_book)
    db.flush()
    return new_book


def update(db: Session, book: BooksDB, book_data: BookPatch) -> BooksDB:
    for field, data in book_data.model_dump(exclude_unset=True).items():
        setattr(book, field, data)
    db.flush()
    return book


def delete_book(db: Session, book: BooksDB) -> None:
    db.delete(book)
    db.flush()
