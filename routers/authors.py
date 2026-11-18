from collections.abc import Sequence

from fastapi import APIRouter, status

from dependencies import SessionDep
from models import AuthorsDB
from repositories import authors as authors_repo
from schemas import (
    AuthorCreate,
    AuthorPatch,
    AuthorPut,
    AuthorResp,
)

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get(
    "",
    summary="Get all authors",
    response_model=list[AuthorResp],
)
def read_authors(db: SessionDep) -> Sequence[AuthorsDB]:
    return authors_repo.get_all_authors(db)


@router.post(
    "",
    summary="Add new author",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResp,
)
def create_author(author: AuthorCreate, db: SessionDep):
    return authors_repo.create_author(db, author)


@router.patch(
    "/{author_id}",
    summary="Update author",
    response_model=AuthorResp,
    status_code=status.HTTP_200_OK,
)
def update_author(author_id: int, author_data: AuthorPatch, db: SessionDep):
    return authors_repo.patch_author(db, author_data, author_id)


@router.put(
    "/{author_id}",
    summary="Full author change",
    status_code=status.HTTP_200_OK,
    response_model=AuthorResp,
)
def change_author(author_id: int, author_data: AuthorPut, db: SessionDep):
    return authors_repo.put_author(db, author_data, author_id)


@router.delete(
    "/{author_id}",
    summary="Delete an author",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(author_id: int, db: SessionDep):
    authors_repo.delete_author(db, author_id)
