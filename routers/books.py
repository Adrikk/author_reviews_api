from fastapi import APIRouter, status

from dependencies import SessionDep
from repositories import books as books_repo
from schemas import (
    BookCreate,
    BookPatch,
    BookPut,
    BookResp,
)

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", summary="Get all books", response_model=list[BookResp])
def read_books(db: SessionDep):
    return books_repo.get_all_books(db)


@router.post(
    "",
    summary="Add a new book",
    response_model=BookResp,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate, db: SessionDep):
    return books_repo.create_book(db, book)


@router.put(
    "/{book_id}",
    summary="Full change the book",
    response_model=BookResp,
)
def change_book(book_id: int, book_data: BookPut, db: SessionDep):
    return books_repo.put_book(db, book_data, book_id)


@router.patch(
    "/{book_id}",
    summary="Partial book update",
    response_model=BookResp,
)
def update_book(book_id: int, book_data: BookPatch, db: SessionDep):
    return books_repo.patch_book(db, book_data, book_id)


@router.delete(
    "/{book_id}",
    summary="Delete the book by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, db: SessionDep):
    books_repo.delete_book(db, book_id)
