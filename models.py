from datetime import datetime

from sqlalchemy import ForeignKey, MetaData, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class AuthorsDB(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    lastname: Mapped[str] = mapped_column(index=True)
    firstname: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now)


class BooksDB(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    is_shown: Mapped[bool] = mapped_column(default=False, server_default=false())
