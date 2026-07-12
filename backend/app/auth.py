from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    x_session_token: Annotated[str | None, Header()] = None,
) -> User:
    if not x_session_token:
        raise HTTPException(status_code=401, detail="missing simulated session")
    user = db.scalar(select(User).where(User.session_token == x_session_token))
    if user is None:
        raise HTTPException(status_code=401, detail="invalid simulated session")
    return user
