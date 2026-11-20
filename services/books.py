from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import AuthorDoesNotExist, BooksNotFoundError, PermissionDeniedError
from models import BooksDB
from repositories import authors as authors_repo
from repositories import books as books_repo
from schemas import BookCreate, BookPatch


def get_all_books(db: Session) -> Sequence[BooksDB]:
    return books_repo.get_all(db)


def get_book(book_id: int, db: Session) -> BooksDB:
    book = books_repo.get_by_id(book_id=book_id, db=db)
    if not book or not book.is_shown:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    return book


def add_new_book(
    author_id: int, book_data: BookCreate, db: Session
) -> BooksDB:
    if not authors_repo.get_by_id(author_id=author_id, db=db):
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    return books_repo.create(author_id=author_id, book_data=book_data, db=db)


def update_book(
    book_id: int, book_data: BookPatch, author_id: int, db: Session
) -> BooksDB:
    book = books_repo.get_by_id(book_id=book_id, db=db)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    if book.author_id != author_id:
        raise PermissionDeniedError("Вы не можете изменять чужие книги")
    return books_repo.update(book=book, book_data=book_data, db=db)


def delete_book(book_id: int, author_id: int, db: Session) -> None:
    book = books_repo.get_by_id(book_id=book_id, db=db)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    if book.author_id != author_id:
        raise PermissionDeniedError("Вы не можете удалять чужие книги")
    books_repo.delete_book(book=book, db=db)
