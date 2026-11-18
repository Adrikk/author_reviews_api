from collections.abc import Sequence

from sqlalchemy import select

from dependencies import Session
from models import AuthorsDB
from schemas import AuthorCreate, AuthorPut


def get_all(db: Session) -> Sequence[AuthorsDB]:
    return db.scalars(select(AuthorsDB)).all()


def get_by_id(author_id: int, db: Session) -> AuthorsDB | None:
    return db.scalar(select(AuthorsDB).where(AuthorsDB.id == author_id))


def create(db: Session, author_data: AuthorCreate) -> AuthorsDB | None:
    new_author = AuthorsDB(**author_data.model_dump())
    db.add(new_author)
    db.flush()
    return new_author


def update(db: Session, author: AuthorsDB, author_data: AuthorPut) -> AuthorsDB:
    for field, data in author_data.model_dump(exclude_unset=True).items():
        setattr(author, field, data)
    db.flush()
    return author


def delete(db: Session, author: AuthorsDB) -> bool | None:
    db.delete(author)
    db.flush()
