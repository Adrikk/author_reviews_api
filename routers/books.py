from fastapi import APIRouter, HTTPException, status

from dependencies import SessionDep
from main import app
from models import BooksDB
from schemas import (
    BookCreate,
    BookPatch,
    BookPut,
    BookResp,
)

router = APIRouter(prefix="/books", tags=["Books"])


# Get all books
@app.get("", tags=["Books"], summary="Get all books", response_model=list[BookResp])
def read_books(db: SessionDep):
    return db.scalars(select(BooksDB)).all()


# Add a new book
@app.post(
    "",
    tags=["Books"],
    summary="Add a new book",
    response_model=BookResp,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate, db: SessionDep):
    # Проверяем, существует ли автор перед созданием книги
    author_exists = db.scalar(select(AuthorsDB).where(AuthorsDB.id == book.author_id))
    if not author_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Автор с id={book.author_id} не найден",
        )

    db_book = BooksDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put(
    "/{book_id}",
    tags=["Books"],
    summary="Full change the book",
    response_model=BookResp,
)
def change_book(book_id: int, book_data: BookPut, db: SessionDep):
    book_db = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not book_db:
        raise HTTPException(status_code=404, detail=f"Книга с ID={book_id} не найдена")
    for field, data in book_data.model_dump().items():
        setattr(book_db, field, data)
    db.commit()
    db.refresh(book_db)
    return book_db


@app.patch(
    "/{book_id}",
    tags=["Books"],
    summary="Full change the book",
    response_model=BookResp,
)
def update_book(book_id: int, book_data: BookPatch, db: SessionDep):
    book_db = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not book_db:
        raise HTTPException(status_code=404, detail=f"Книга с ID={book_id} не найдена")
    for field, data in book_data.model_dump(exclude_unset=True).items():
        setattr(book_db, field, data)
    db.commit()
    db.refresh(book_db)
    return book_db


@app.delete(
    "/{book_id}",
    tags=["Books"],
    summary="Delete the book by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, db: SessionDep):
    book_db = db.scalar(select(BooksDB).filter(BooksDB.id == book_id))
    if not book_db:
        raise HTTPException(status_code=404, detail=f"Книга с ID={book_id} не найдена")

    db.delete(book_db)
    db.commit()
