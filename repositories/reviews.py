from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import ReviewsDB
from schemas import ReviewCreate, ReviewPatch


def get_all_by_book(db: Session, book_id: int) -> Sequence[ReviewsDB]:
    return db.scalars(
        select(ReviewsDB).where(
            ReviewsDB.book_id == book_id, ReviewsDB.is_shown.is_(True)
        )
    ).all()


def get_by_id(db: Session, book_id: int, review_id: int) -> ReviewsDB | None:
    return db.scalar(
        select(ReviewsDB).where(ReviewsDB.id == review_id, ReviewsDB.book_id == book_id)
    )


def create(db: Session, review_data: ReviewCreate, book_id: int) -> ReviewsDB:
    new_review = ReviewsDB(**review_data.model_dump(), book_id=book_id)
    db.add(new_review)
    db.flush()
    return new_review


def update(db: Session, review: ReviewsDB, review_data: ReviewPatch) -> ReviewsDB:
    for field, data in review_data.model_dump(exclude_unset=True).items():
        setattr(review, field, data)
    db.flush()
    return review


def delete(db: Session, db_review: ReviewsDB) -> None:
    db.delete(db_review)
    db.flush()


def get_average_rating(db: Session, book_id: int) -> float:
    avg = db.scalar(
        select(func.avg(ReviewsDB.rating)).where(
            ReviewsDB.book_id == book_id, ReviewsDB.is_shown.is_(True)
        )
    )
    return round(float(avg), 2) if avg is not None else 0.0
