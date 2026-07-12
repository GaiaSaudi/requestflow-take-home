from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ChangeRequest, DecisionHistory, User
from app.schemas import (
    ChangeRequestOut,
    DecisionHistoryOut,
    StarterDecisionIn,
    StarterDecisionOut,
    UserOut,
)
from app.service import decide_request_legacy

app = FastAPI(title="RequestFlow Starter API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Db = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/session", response_model=UserOut)
def session(current_user: CurrentUser) -> User:
    return current_user


@app.get("/api/requests", response_model=list[ChangeRequestOut])
def list_requests(db: Db, current_user: CurrentUser) -> list[ChangeRequest]:
    statement = (
        select(ChangeRequest)
        .where(
            or_(
                ChangeRequest.requester_id == current_user.id,
                ChangeRequest.assigned_reviewer_id == current_user.id,
                ChangeRequest.reviewer_team_id == current_user.team_id,
            )
        )
        .order_by(ChangeRequest.id)
    )
    return list(db.scalars(statement))


def visible_request_or_404(db: Session, current_user: User, request_id: int) -> ChangeRequest:
    request = db.get(ChangeRequest, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="request not found")
    if not (
        request.requester_id == current_user.id
        or request.assigned_reviewer_id == current_user.id
        or request.reviewer_team_id == current_user.team_id
    ):
        raise HTTPException(status_code=404, detail="request not found")
    return request


@app.get("/api/requests/{request_id}", response_model=ChangeRequestOut)
def get_request(request_id: int, db: Db, current_user: CurrentUser) -> ChangeRequest:
    return visible_request_or_404(db, current_user, request_id)


@app.get("/api/requests/{request_id}/history", response_model=list[DecisionHistoryOut])
def get_history(
    request_id: int,
    db: Db,
    current_user: CurrentUser,
) -> list[DecisionHistory]:
    visible_request_or_404(db, current_user, request_id)
    return list(
        db.scalars(
            select(DecisionHistory)
            .where(DecisionHistory.request_id == request_id)
            .order_by(DecisionHistory.id)
        )
    )


@app.post("/api/requests/{request_id}/decision", response_model=StarterDecisionOut)
def decide_request(
    request_id: int,
    payload: StarterDecisionIn,
    db: Db,
    current_user: CurrentUser,
) -> StarterDecisionOut:
    request = visible_request_or_404(db, current_user, request_id)
    decided, history = decide_request_legacy(db, request, payload)
    return StarterDecisionOut(request=decided, history=history)
