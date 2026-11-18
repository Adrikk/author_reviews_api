from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import BooksNotFoundError
from models import BooksDB
from repositories import books as books_repo
from schemas import BookCreate


def get_all_books(db: Session) -> Sequence[BooksDB]:
    all_books = books_repo.get_all(db)
    if not all_books:
        raise BooksNotFoundError("Книг нет")
    return all_books


def get_book(db: Session, book_id: int):
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    return book

def add_new_book(db: Session, book_data: BooksCreate) -> BooksDB:
