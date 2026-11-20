from collections.abc import Sequence

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from models import AuthorsDB
from schemas import AuthorCreateDB, AuthorPatch


def get_all(db: Session) -> Sequence[AuthorsDB]:
    return db.scalars(select(AuthorsDB)).all()


def get_by_id(author_id: int, db: Session) -> AuthorsDB | None:
    return db.scalar(select(AuthorsDB).where(AuthorsDB.id == author_id))


def get_by_username_or_email(
    username: str | None = None,
    email: str | None = None,
    exclude_id: int | None = None,
    *,
    db: Session,
) -> AuthorsDB | None:
    conditions = []
    if username is not None:
        conditions.append(AuthorsDB.username == username)
    if email is not None:
        conditions.append(AuthorsDB.email == email)

    if not conditions:
        return None

    req = select(AuthorsDB).where(or_(*conditions))
    if exclude_id is not None:
        req = req.where(AuthorsDB.id != exclude_id)
    return db.scalar(req)


def create(author_data: AuthorCreateDB, db: Session) -> AuthorsDB:
    new_author = AuthorsDB(**author_data.model_dump())
    db.add(new_author)
    db.flush()
    return new_author


def update(
    author: AuthorsDB, author_data: AuthorPatch, db: Session
) -> AuthorsDB:
    for field, data in author_data.model_dump(exclude_unset=True).items():
        setattr(author, field, data)
    db.flush()
    return author


def delete(author: AuthorsDB, db: Session) -> None:
    db.delete(author)
    db.flush()
