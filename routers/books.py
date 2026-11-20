from fastapi import APIRouter, status

from dependencies import CurrentAuthorDep, SessionDep
from schemas import (
    BookCreate,
    BookPatch,
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


@router.get("/{book_id}", summary="Get book", response_model=BookResp)
def read_book(book_id: int, db: SessionDep):
    return books_serv.get_book(book_id, db)


@router.post(
    "",
    summary="Add a new book",
    response_model=BookResp,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book_data: BookCreate, current_author: CurrentAuthorDep, db: SessionDep
):
    return books_serv.add_new_book(
        author_id=current_author.id, book_data=book_data, db=db
    )


@router.patch(
    "/{book_id}",
    summary="Partial book update",
    response_model=BookResp,
)
def update_book(
    book_id: int,
    book_data: BookPatch,
    current_author: CurrentAuthorDep,
    db: SessionDep,
):
    return books_serv.update_book(
        book_id=book_id,
        book_data=book_data,
        author_id=current_author.id,
        db=db,
    )


@router.delete(
    "/{book_id}",
    summary="Delete the book by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int, current_author: CurrentAuthorDep, db: SessionDep
):
    books_serv.delete_book(
        book_id=book_id, author_id=current_author.id, db=db
    )
