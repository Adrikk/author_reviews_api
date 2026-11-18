from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import AuthorDoesNotExist
from models import AuthorsDB
from repositories import authors as authors_repo
from schemas import AuthorCreate, AuthorPatch


def get_all_authors(db: Session) -> Sequence[AuthorsDB]:
    authors = authors_repo.get_all(db)
    if not authors:
        raise AuthorDoesNotExist("Список авторов пуст")
    return authors


def get_author(db: Session, author_id: int) -> AuthorsDB:
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    return author


def create_author(db: Session, author_data: AuthorCreate) -> AuthorsDB:
    return authors_repo.create(db, author_data)


def update_author(db: Session, author_id: int, author_data: AuthorPatch) -> AuthorsDB:
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    return authors_repo.update(db, author, author_data)


def delete_author(db: Session, author_id: int):
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    authors_repo.delete(db, author)
