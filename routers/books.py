from fastapi import APIRouter, Query, status

from dependencies import SessionDep
from schemas import (
    BookCreate,
    BookPatch,
    BookPut,
    BookResp,
)
from services import books as books_serv

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "",
    summary="Get all books",
    response_model=list[BookResp],
)
def read_books(db: SessionDep):
    return books_serv.get_all_books(db)


@router.post(
    "",
    summary="Add a new book",
    response_model=BookResp,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate, db: SessionDep, author_id: int = Query(..., ge=1)):
    return books_serv.add_new_book(db, author_id, book)


@router.put(
    "/{book_id}",
    summary="Replace the book",
    response_model=BookResp,
)
def replace_book(book_id: int, book_data: BookPut, db: SessionDep):
    return books_serv.update_book(db, book_id, book_data)


@router.patch(
    "/{book_id}",
    summary="Partial book update",
    response_model=BookResp,
)
def update_book(book_id: int, book_data: BookPatch, db: SessionDep):
    return books_serv.update_book(db, book_id, book_data)


@router.delete(
    "/{book_id}",
    summary="Delete the book by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, db: SessionDep):
    books_serv.delete_book(db, book_id)
