from typing import Optional

import jwt
from fastapi import Header, HTTPException

from .config import JWT_SECRET


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def username_from_header(authorization: Optional[str]) -> Optional[str]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    payload = decode_token(authorization[7:].strip())
    if not payload or "user" not in payload:
        return None
    return payload["user"]


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    username = username_from_header(authorization)
    if not username:
        raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
    return username


def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[str]:
    return username_from_header(authorization)
