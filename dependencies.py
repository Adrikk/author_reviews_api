from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from core import security
from database import LocalSession
from exceptions import (
    ConflictError,
    CredentialsError,
    DatabaseError,
)
from models import AuthorsDB
from repositories import authors as author_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = LocalSession()
    try:
        yield db
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        # Например, сработал UniqueConstraint при одновременных запросах
        raise ConflictError("Конфликт данных при сохранении") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise DatabaseError("Ошибка при работе с базой данных") from exc
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_author(
    token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep
) -> AuthorsDB:
    try:
        payload = security.decode_access_token(token)
        author_id = payload.get("sub")
        if author_id is None:
            raise CredentialsError
        author_id = int(author_id)
    except (jwt.InvalidTokenError, ValueError):
        raise CredentialsError
    author = author_repo.get_by_id(author_id=author_id, db=db)
    if not author:
        raise CredentialsError
    return author


CurrentAuthorDep = Annotated[AuthorsDB, Depends(get_current_author)]
