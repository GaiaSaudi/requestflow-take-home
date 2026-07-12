from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base, ChangeRequest, Team, User


@pytest.fixture
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)

    with testing_session.begin() as db:
        db.add(Team(id=1, name="Platform"))
        db.add_all(
            [
                User(
                    id=1,
                    name="Alice",
                    team_id=1,
                    is_reviewer=False,
                    session_token="session-alice",
                ),
                User(
                    id=2,
                    name="Bob",
                    team_id=1,
                    is_reviewer=True,
                    session_token="session-bob",
                ),
            ]
        )
        db.add(
            ChangeRequest(
                id=1,
                title="Example request",
                description="A deterministic starter request.",
                requester_id=1,
                assigned_reviewer_id=2,
                reviewer_team_id=1,
            )
        )

    def override_db() -> Iterator[Session]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
