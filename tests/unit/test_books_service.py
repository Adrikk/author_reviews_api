from unittest.mock import Mock

import pytest

from exceptions import AuthorDoesNotExist
from schemas import BookCreate
from services import books as books_service


def test_add_book_rejects_missing_author(monkeypatch):
    db = Mock()
    book_data = BookCreate(name="My Book", description="Book description")
    create_book = Mock()
    monkeypatch.setattr(
        books_service.authors_repo, "get_by_id", Mock(return_value=None)
    )
    monkeypatch.setattr(books_service.books_repo, "create", create_book)

    with pytest.raises(AuthorDoesNotExist):
        books_service.add_new_book(db, author_id=123, book_data=book_data)

    create_book.assert_not_called()


def test_add_book_uses_repository_for_existing_author(monkeypatch):
    db = Mock()
    author = object()
    book = object()
    book_data = BookCreate(name="My Book", description="Book description")
    create_book = Mock(return_value=book)
    monkeypatch.setattr(
        books_service.authors_repo, "get_by_id", Mock(return_value=author)
    )
    monkeypatch.setattr(books_service.books_repo, "create", create_book)

    result = books_service.add_new_book(db, author_id=7, book_data=book_data)

    assert result is book
    create_book.assert_called_once_with(db, book_data, 7)
