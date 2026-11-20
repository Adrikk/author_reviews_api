from fastapi import APIRouter, status

from dependencies import CurrentAuthorDep, SessionDep
from schemas import (
    ReviewCreate,
    ReviewPatch,
    ReviewResp,
)
from services import reviews as reviews_serv

router = APIRouter(prefix="/books/{book_id}/reviews", tags=["Reviews"])


@router.get("", summary="Get all reviews of the book", response_model=list[ReviewResp])
def read_reviews(book_id: int, db: SessionDep):
    return reviews_serv.get_book_reviews(book_id=book_id, db=db)


@router.get("/{review_id}", summary="Get review", response_model=ReviewResp)
def read_review(book_id: int, review_id: int, db: SessionDep):
    return reviews_serv.get_review(book_id=book_id, review_id=review_id, db=db)


@router.post(
    "",
    summary="Add new review",
    response_model=ReviewResp,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    book_id: int,
    review_data: ReviewCreate,
    current_author: CurrentAuthorDep,
    db: SessionDep,
):
    return reviews_serv.add_new_review(
        book_id=book_id,
        review_data=review_data,
        author_id=current_author.id,
        db=db,
    )


@router.patch(
    "/{review_id}",
    summary="Update review",
    response_model=ReviewResp,
)
def update_review(
    book_id: int,
    review_id: int,
    review_data: ReviewPatch,
    current_author: CurrentAuthorDep,
    db: SessionDep,
):
    return reviews_serv.update_review(
        book_id=book_id,
        review_id=review_id,
        review_data=review_data,
        author_id=current_author.id,
        db=db,
    )


@router.delete(
    "/{review_id}",
    summary="Delete the review with ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    book_id: int,
    review_id: int,
    current_author: CurrentAuthorDep,
    db: SessionDep,
):
    reviews_serv.delete_review(
        book_id=book_id,
        review_id=review_id,
        author_id=current_author.id,
        db=db,
    )
