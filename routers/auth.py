from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import services.authors as authors_serv
from core import security
from dependencies import SessionDep
from schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login_author(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep
):
    author = authors_serv.authenticate_author(
        db, form_data.username, form_data.password
    )
    token = security.create_access_token(author.id)
    return Token(access_token=token)
