from fastapi import APIRouter, status

from dependencies import SessionDep
from schemas import (
    ReviewCreate,
    ReviewPatch,
    ReviewResp,
)
from services import reviews as reviews_serv

router = APIRouter(prefix="/books/{book_id}/reviews", tags=["Reviews"])


@router.get("", summary="Get all reviews of the book", response_model=list[ReviewResp])
def read_reviews(db: SessionDep, book_id: int):
    return reviews_serv.get_book_reviews(db, book_id)


@router.get("/{review_id}", summary="Get review", response_model=ReviewResp)
def read_review(db: SessionDep, book_id: int, review_id: int):
    return reviews_serv.get_review(db, book_id, review_id)


@router.post(
    "",
    summary="Add new review",
    response_model=ReviewResp,
    status_code=status.HTTP_201_CREATED,
)
def create_review(db: SessionDep, review_data: ReviewCreate, book_id: int):
    return reviews_serv.add_new_review(db, book_id, review_data)


@router.patch(
    "/{review_id}",
    summary="Update review",
    response_model=ReviewResp,
)
def update_review(
    db: SessionDep, review_id: int, book_id: int, review_data: ReviewPatch
):
    return reviews_serv.update_review(db, book_id, review_id, review_data)


@router.delete(
    "/{review_id}",
    summary="Delete the review with ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(db: SessionDep, review_id: int, book_id: int):
    reviews_serv.delete_review(db, book_id, review_id)
