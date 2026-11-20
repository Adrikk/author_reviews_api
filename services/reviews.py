from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import (
    BooksNotFoundError,
    PermissionDeniedError,
    ReviewsNotFoundError,
)
from models import BooksDB, ReviewsDB
from repositories import books as books_repo
from repositories import reviews as reviews_repo
from schemas import ReviewCreate, ReviewPatch


def _get_book_or_404(
    book_id: int, db: Session, only_shown: bool = False
) -> BooksDB:
    book = books_repo.get_by_id(book_id=book_id, db=db)
    if not book or (only_shown and not book.is_shown):
        raise BooksNotFoundError(f"Книга с ID={book_id} не существует")
    return book


def _get_review_or_404(
    book_id: int, review_id: int, db: Session, only_shown: bool = False
) -> ReviewsDB:
    review = reviews_repo.get_by_id(book_id=book_id, review_id=review_id, db=db)
    if not review or (only_shown and not review.is_shown):
        raise ReviewsNotFoundError(f"Отзыв c ID={review_id} не найден")
    return review


def get_book_reviews(book_id: int, db: Session) -> Sequence[ReviewsDB]:
    _get_book_or_404(book_id, db, only_shown=True)
    return reviews_repo.get_all_by_book(book_id=book_id, db=db)


def get_review(book_id: int, review_id: int, db: Session) -> ReviewsDB:
    _get_book_or_404(book_id, db, only_shown=True)
    return _get_review_or_404(book_id, review_id, db, only_shown=True)


def add_new_review(
    book_id: int,
    review_data: ReviewCreate,
    author_id: int,
    db: Session,
) -> ReviewsDB:
    book = _get_book_or_404(book_id, db, only_shown=True)
    if book.author_id == author_id:
        raise PermissionDeniedError("Вы не можете добавлять отзыв на свои книги")

    new_review = reviews_repo.create(
        book_id=book_id,
        author_id=author_id,
        review_data=review_data,
        db=db,
    )
    book.rating = reviews_repo.get_average_rating(book_id=book_id, db=db)
    return new_review


def update_review(
    book_id: int,
    review_id: int,
    review_data: ReviewPatch,
    author_id: int,
    db: Session,
) -> ReviewsDB:
    book = _get_book_or_404(book_id, db)
    review = _get_review_or_404(book_id, review_id, db)

    if review.author_id != author_id:
        raise PermissionDeniedError("Вы не можете редактировать чужие отзывы")

    updated_review = reviews_repo.update(
        review=review, review_data=review_data, db=db
    )

    if {"rating", "is_shown"} & review_data.model_fields_set:
        book.rating = reviews_repo.get_average_rating(book_id=book_id, db=db)

    return updated_review


def delete_review(
    book_id: int, review_id: int, author_id: int, db: Session
) -> None:
    book = _get_book_or_404(book_id, db)
    review = _get_review_or_404(book_id, review_id, db)

    if review.author_id != author_id:
        raise PermissionDeniedError("Вы не можете удалять чужие отзывы")

    reviews_repo.delete(db_review=review, db=db)
    book.rating = reviews_repo.get_average_rating(book_id=book_id, db=db)
