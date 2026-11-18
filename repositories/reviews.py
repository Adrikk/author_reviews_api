from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from dependencies import Session
from exceptions import AppExceptions, BooksNotFoundError, ReviewsNotFoundError
from models import ReviewsDB
from schemas import ReviewCreate, ReviewPatch


def get_all_book_reviews(db: Session, book_id: int) -> Sequence[ReviewsDB]:
    return db.scalars(select(ReviewsDB).where(ReviewsDB.book_id == book_id)).all()


def get_review_by_id(db: Session, book_id: int, review_id: int) -> ReviewsDB | None:
    review = db.scalar(
        select(ReviewsDB).where(ReviewsDB.id == review_id, ReviewsDB.book_id == book_id)
    )
    if not review:
        raise ReviewsNotFoundError("Отзыв не найден.")
    return review


def create_review(db: Session, review_data: ReviewCreate, book_id: int) -> ReviewsDB:
    new_review = ReviewsDB(**review_data.model_dump(), book_id=book_id)
    db.add(new_review)
    try:
        db.commit()
        db.refresh(new_review)
        return new_review
    except IntegrityError as e:
        db.rollback()
        raise BooksNotFoundError(
            f"Отзыв не может быть добавлен. Книга с ID={book_id} не найдена."
        ) from e


def patch_review(
    db: Session, review_data: ReviewPatch, book_id: int, review_id: int
) -> ReviewsDB:
    db_review = get_review_by_id(db, book_id, review_id)
    if not db_review:
        raise ReviewsNotFoundError("Отзыв не найден")
    for field, data in review_data.model_dump(exclude_unset=True).items():
        setattr(db_review, field, data)
    try:
        db.commit()
        db.refresh(db_review)
        return db_review
    except IntegrityError as e:
        db.rollback()
        raise AppExceptions("Возникла проблема при добавлении отзыва") from e


def delete_review(db: Session, book_id: int, review_id: int) -> None:
    db_review = get_review_by_id(db, book_id, review_id)
    if not db_review:
        raise ReviewsNotFoundError("Отзыв не найден")
    db.delete(db_review)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise AppExceptions("Не удалось удалить отзыв. Попробуйте ещё раз") from e
