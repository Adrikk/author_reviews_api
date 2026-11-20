from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import ReviewsDB
from schemas import ReviewCreate, ReviewPatch


def get_all_by_book(book_id: int, db: Session) -> Sequence[ReviewsDB]:
    return db.scalars(
        select(ReviewsDB).where(
            ReviewsDB.book_id == book_id, ReviewsDB.is_shown.is_(True)
        )
    ).all()


def get_by_id(book_id: int, review_id: int, db: Session) -> ReviewsDB | None:
    return db.scalar(
        select(ReviewsDB).where(ReviewsDB.id == review_id, ReviewsDB.book_id == book_id)
    )


def create(
    book_id: int, author_id: int, review_data: ReviewCreate, db: Session
) -> ReviewsDB:
    new_review = ReviewsDB(
        **review_data.model_dump(), book_id=book_id, author_id=author_id
    )
    db.add(new_review)
    db.flush()
    return new_review


def update(
    review: ReviewsDB, review_data: ReviewPatch, db: Session
) -> ReviewsDB:
    for field, data in review_data.model_dump(exclude_unset=True).items():
        setattr(review, field, data)
    db.flush()
    return review


def delete(db_review: ReviewsDB, db: Session) -> None:
    db.delete(db_review)
    db.flush()


def get_average_rating(book_id: int, db: Session) -> float:
    avg = db.scalar(
        select(func.avg(ReviewsDB.rating)).where(
            ReviewsDB.book_id == book_id, ReviewsDB.is_shown.is_(True)
        )
    )
    return round(float(avg), 2) if avg is not None else 0.0
