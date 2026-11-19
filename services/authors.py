from collections.abc import Sequence

from sqlalchemy.orm import Session

from exceptions import AuthorDoesNotExist, ConflictError
from models import AuthorsDB
from repositories import authors as authors_repo
from schemas import AuthorCreate, AuthorPatch, AuthorPut


def get_all_authors(db: Session) -> Sequence[AuthorsDB]:
    return authors_repo.get_all(db)


def get_author(db: Session, author_id: int) -> AuthorsDB:
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    return author


def create_author(db: Session, author_data: AuthorCreate) -> AuthorsDB:
    existing_author = authors_repo.get_by_username_or_email(
        db, author_data.username, author_data.email
    )
    if existing_author:
        if existing_author.username == author_data.username:
            raise ConflictError(
                f"Пользователь с username={author_data.username} уже существует"
            )
        raise ConflictError(f"Пользователь с email={author_data.email} уже существует")
    return authors_repo.create(db, author_data)


def update_author(
    db: Session, author_id: int, author_data: AuthorPatch | AuthorPut
) -> AuthorsDB:
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    if author_data.username is not None or author_data.email is not None:
        existed_author = authors_repo.get_by_username_or_email(
            db, author_data.username, author_data.email, exclude_id=author.id
        )
        if existed_author:
            if author_data.username and existed_author.username == author_data.username:
                raise ConflictError(
                    f"Пользователь с username={author_data.username} уже существует"
                )
            raise ConflictError(
                f"Пользователь с email={author_data.email} уже существует"
            )

    return authors_repo.update(db, author, author_data)


def delete_author(db: Session, author_id: int):
    author = authors_repo.get_by_id(db, author_id)
    if not author:
        raise AuthorDoesNotExist(f"Автор с ID={author_id} не найден")
    authors_repo.delete(db, author)
