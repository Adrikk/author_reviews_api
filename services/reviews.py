from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import AuthorDoesNotExist, BooksNotFoundError, ReviewsNotFoundError
from models import ReviewsDB
from repositories import authors as authors_repo
from repositories import books as books_repo
from repositories import reviews as reviews_repo
from schemas import ReviewCreate, ReviewPatch


def get_book_reviews(db: Session, book_id: int) -> Sequence[ReviewsDB]:
    book = books_repo.get_by_id(db, book_id)
    if not book or not book.is_shown:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    return reviews_repo.get_all_by_book(db, book_id)


def get_review(db: Session, book_id: int, review_id: int) -> ReviewsDB:
    book = books_repo.get_by_id(db, book_id)
    if not book or not book.is_shown:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    review = reviews_repo.get_by_id(db, book_id, review_id)
    if not review or not review.is_shown:
        raise ReviewsNotFoundError(f"Отзыв с ID={review_id} не найден у данной книги")
    return review


def add_new_review(db: Session, book_id: int, review_data: ReviewCreate) -> ReviewsDB:
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга с ID={book_id} не найдена")
    if not authors_repo.get_by_id(db, review_data.author_id):
        raise AuthorDoesNotExist(f"Автор с ID={review_data.author_id} не найден")
    new_review = reviews_repo.create(db, review_data, book_id)

    # Update book rating
    book.rating = reviews_repo.get_average_rating(db, book_id)
    return new_review


def update_review(
    db: Session, book_id: int, review_id: int, review_data: ReviewPatch
) -> ReviewsDB:
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга c ID={book_id} не найдена")
    review = reviews_repo.get_by_id(db, book_id, review_id)
    if not review:
        raise ReviewsNotFoundError(f"Отзыв с ID={review_id} не найден у данной книги")
    updated_review = reviews_repo.update(db, review, review_data)

    if {"rating", "is_shown"} & review_data.model_fields_set:
        book.rating = reviews_repo.get_average_rating(db, book_id)

    return updated_review


def delete_review(db: Session, book_id: int, review_id: int):
    book = books_repo.get_by_id(db, book_id)
    if not book:
        raise BooksNotFoundError(f"Книга c ID={book_id} не найдена")
    review = reviews_repo.get_by_id(db, book_id, review_id)
    if not review:
        raise ReviewsNotFoundError(f"Отзыв с ID={review_id} не найден у данной книги")
    reviews_repo.delete(db, review)

    book.rating = reviews_repo.get_average_rating(db, book_id)
