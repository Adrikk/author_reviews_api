from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from core import config


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    password_hash = PasswordHash.recommended()

    hashed = password_hash.hash(password)

    return hashed


def verify_password(password: str, hashed: str) -> bool:
    """Verify a stored password against one provided by user"""
    password_hash = PasswordHash.recommended()

    return password_hash.verify(password, hashed)


def create_access_token(subject: str | int) -> str:
    to_encode = {
        "sub": str(subject),
        "exp": datetime.now(UTC)
        + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(to_encode, key=config.SECRET_KEY, algorithm=config.ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
