from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import AuthorDoesNotExist, BooksNotFoundError
from models import BooksDB
from repositories import authors as authors_repo
from repositories import books as books_repo
from schemas import BookCreate, BookPatch, BookPut


def get_all_books(db: Session) -> Sequence[BooksDB]:
    return books_repo.get_all(db)


def get_book(db: Session, book_id: int):
    book = books_repo.get_by_id(db, book_id)
    if not book or not book.is_shown:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    return book


def add_new_book(db: Session, author_id: int, book_data: BookCreate) -> BooksDB:
    if not authors_repo.get_by_id(db, author_id):
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    return books_repo.create(db, book_data, author_id)


def update_book(
    db: Session, book_id: int, book_data: BookPatch | BookPut
) -> BooksDB:
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    return books_repo.update(db, book, book_data)


def delete_book(db: Session, book_id: int):
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    books_repo.delete_book(db, book)
