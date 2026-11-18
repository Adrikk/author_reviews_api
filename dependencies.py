from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database import LocalSession
from exceptions import ConflictError, DatabaseError


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
