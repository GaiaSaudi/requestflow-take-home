from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import ChangeRequest, DecisionHistory, User, utc_now
from app.schemas import StarterDecisionIn


def decide_request_legacy(
    db: Session,
    request: ChangeRequest,
    payload: StarterDecisionIn,
) -> tuple[ChangeRequest, DecisionHistory]:
    """Intentionally incomplete starter implementation for the take-home."""
    actor = db.get(User, payload.actor_id)
    if actor is None:
        raise HTTPException(status_code=400, detail="unknown actor")
    if request.status != "pending":
        raise HTTPException(status_code=409, detail="request is no longer pending")

    request.status = payload.decision
    request.version += 1
    request.decision_note = payload.reason
    request.decided_by_id = actor.id
    request.decided_at = utc_now()
    db.add(request)
    db.commit()
    db.refresh(request)

    history = DecisionHistory(
        request_id=request.id,
        actor_id=actor.id,
        decision=payload.decision,
        note=payload.reason,
        idempotency_key=payload.idempotency_key,
        request_version=request.version,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return request, history
