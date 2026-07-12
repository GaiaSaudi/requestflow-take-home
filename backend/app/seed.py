from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from app.database import SessionLocal
from app.models import ChangeRequest, DecisionHistory, Team, User


def seed() -> None:
    with SessionLocal.begin() as db:
        if db.scalar(select(User.id).limit(1)) is not None:
            return

        platform = Team(id=1, name="Platform")
        operations = Team(id=2, name="Operations")
        db.add_all([platform, operations])

        users = [
            User(
                id=1,
                name="Alice Requester",
                team_id=1,
                is_reviewer=False,
                session_token="session-alice",
            ),
            User(
                id=2, name="Bob Reviewer", team_id=1, is_reviewer=True, session_token="session-bob"
            ),
            User(
                id=3,
                name="Carol Reviewer",
                team_id=1,
                is_reviewer=True,
                session_token="session-carol",
            ),
            User(
                id=4,
                name="Dana Outsider",
                team_id=2,
                is_reviewer=True,
                session_token="session-dana",
            ),
            User(
                id=5,
                name="Erin Dual Role",
                team_id=1,
                is_reviewer=True,
                session_token="session-erin",
            ),
        ]
        db.add_all(users)

        decided_at = datetime(2026, 1, 10, 9, 30, tzinfo=UTC)
        requests = [
            ChangeRequest(
                id=1,
                title="Increase worker concurrency",
                description="Raise the reporting worker concurrency from 4 to 8.",
                requester_id=1,
                assigned_reviewer_id=2,
                reviewer_team_id=1,
                status="pending",
                version=1,
            ),
            ChangeRequest(
                id=2,
                title="Rotate integration credentials",
                description=(
                    "Rotate the staging integration credentials during the maintenance window."
                ),
                requester_id=5,
                assigned_reviewer_id=5,
                reviewer_team_id=1,
                status="pending",
                version=1,
            ),
            ChangeRequest(
                id=3,
                title="Archive legacy dashboard",
                description=(
                    "Remove the unused legacy dashboard after the retention export completes."
                ),
                requester_id=1,
                assigned_reviewer_id=2,
                reviewer_team_id=1,
                status="approved",
                version=2,
                decision_note="Retention export verified.",
                decided_by_id=2,
                decided_at=decided_at,
            ),
            ChangeRequest(
                id=4,
                title="Change operations on-call handoff",
                description="Move the weekend handoff from 08:00 to 09:00 UTC.",
                requester_id=4,
                assigned_reviewer_id=4,
                reviewer_team_id=2,
                status="pending",
                version=1,
            ),
        ]
        db.add_all(requests)
        db.add(
            DecisionHistory(
                request_id=3,
                actor_id=2,
                decision="approved",
                note="Retention export verified.",
                idempotency_key="seed-approved-request-3",
                request_version=2,
                created_at=decided_at,
            )
        )


if __name__ == "__main__":
    seed()
