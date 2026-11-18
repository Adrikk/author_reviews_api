from fastapi import APIRouter, status

from dependencies import SessionDep
from exceptions import ReviewsNotFoundError
from repositories import reviews as reviews_repo
from schemas import (
    ReviewCreate,
    ReviewPatch,
    ReviewResp,
)

router = APIRouter(prefix="/books/{book_id}/reviews", tags=["Reviews"])


@router.get("", summary="Get all reviews of the book", response_model=list[ReviewResp])
def read_reviews(db: SessionDep, book_id: int):
    return reviews_repo.get_all_book_reviews(db, book_id)


@router.get("/{review_id}", summary="Get review", response_model=ReviewResp)
def read_review(db: SessionDep, book_id: int, review_id: int):
    review = reviews_repo.get_review_by_id(db, book_id, review_id)
    if not review:
        raise ReviewsNotFoundError("Отзыв не найден")
    return review


@router.post(
    "",
    summary="Add new review",
    response_model=ReviewResp,
    status_code=status.HTTP_201_CREATED,
)
def create_review(db: SessionDep, review: ReviewCreate, book_id: int):
    return reviews_repo.create_review(db, review, book_id)


@router.patch(
    "/{review_id}",
    summary="Update review",
    response_model=ReviewResp,
)
def update_review(
    db: SessionDep, review_id: int, book_id: int, review_data: ReviewPatch
):
    return reviews_repo.patch_review(db, review_data, review_id, book_id)


@router.delete(
    "/{review_id}",
    summary="Delete the review with ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(db: SessionDep, review_id: int, book_id: int):
    reviews_repo.delete_review(db, review_id, book_id)
