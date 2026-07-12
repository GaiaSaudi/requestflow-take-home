from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    team_id: int
    is_reviewer: bool


class ChangeRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    requester_id: int
    assigned_reviewer_id: int | None
    reviewer_team_id: int
    status: str
    version: int
    decision_note: str | None
    decided_by_id: int | None
    created_at: datetime
    decided_at: datetime | None


class DecisionHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    actor_id: int
    decision: str
    note: str | None
    idempotency_key: str
    request_version: int
    created_at: datetime


class StarterDecisionIn(BaseModel):
    """Legacy starter payload. Its trust assumptions are part of the exercise."""

    actor_id: int
    decision: Literal["approved", "rejected"]
    reason: str | None = None
    idempotency_key: str = Field(min_length=1, max_length=100)
    expected_version: int = Field(ge=1)


class StarterDecisionOut(BaseModel):
    request: ChangeRequestOut
    history: DecisionHistoryOut
