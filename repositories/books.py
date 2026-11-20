from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import BooksDB
from schemas import BookCreate, BookPatch


def get_all(db: Session) -> Sequence[BooksDB]:
    return db.scalars(select(BooksDB).where(BooksDB.is_shown.is_(True))).all()


def get_by_id(book_id: int, db: Session) -> BooksDB | None:
    return db.scalar(select(BooksDB).where(BooksDB.id == book_id))


def create(author_id: int, book_data: BookCreate, db: Session) -> BooksDB:
    new_book = BooksDB(**book_data.model_dump(), author_id=author_id)
    db.add(new_book)
    db.flush()
    return new_book


def update(book: BooksDB, book_data: BookPatch, db: Session) -> BooksDB:
    for field, data in book_data.model_dump(exclude_unset=True).items():
        setattr(book, field, data)
    db.flush()
    return book


def delete_book(book: BooksDB, db: Session) -> None:
    db.delete(book)
    db.flush()
