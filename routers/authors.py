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
def get_author(author_id: int, db: SessionDep):
    return authors_serv.get_author(author_id=author_id, db=db)


@router.post(
    "",
    summary="Add new author",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResp,
)
def create_author(author: AuthorCreate, db: SessionDep):
    return authors_serv.create_author(author_data=author, db=db)


@router.patch(
    "/{author_id}",
    summary="Update author",
    response_model=AuthorResp,
    status_code=status.HTTP_200_OK,
)
def update_author(author_id: int, author_data: AuthorPatch, db: SessionDep):
    return authors_serv.update_author(
        author_id=author_id, author_data=author_data, db=db
    )


@router.delete(
    "/{author_id}",
    summary="Delete an author",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(author_id: int, db: SessionDep):
    authors_serv.delete_author(author_id=author_id, db=db)
