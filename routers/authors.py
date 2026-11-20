from fastapi import APIRouter, status

from dependencies import SessionDep
from schemas import (
    AuthorCreate,
    AuthorPatch,
    AuthorResp,
)
from services import authors as authors_serv

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get(
    "",
    summary="Get all authors",
    response_model=list[AuthorResp],
)
def get_authors(db: SessionDep):
    return authors_serv.get_all_authors(db)


@router.get(
    "/{author_id}",
    summary="Get author",
    response_model=AuthorResp,
)
def get_author(db: SessionDep, author_id: int):
    return authors_serv.get_author(db, author_id)


@router.post(
    "",
    summary="Add new author",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResp,
)
def create_author(author: AuthorCreate, db: SessionDep):
    return authors_serv.create_author(db, author)


@router.patch(
    "/{author_id}",
    summary="Update author",
    response_model=AuthorResp,
    status_code=status.HTTP_200_OK,
)
def update_author(author_id: int, author_data: AuthorPatch, db: SessionDep):
    return authors_serv.update_author(db, author_id, author_data)


@router.delete(
    "/{author_id}",
    summary="Delete an author",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(db: SessionDep, author_id: int):
    authors_serv.delete_author(db, author_id)
