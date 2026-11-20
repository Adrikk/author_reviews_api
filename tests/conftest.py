import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv(
        "SECRET_KEY", "test-only-signing-key-not-for-production-123456"
    )

    from dependencies import get_db
    from main import app
    from models import Base

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    test_session = sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )

    def override_get_db():
        db = test_session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)
        Base.metadata.drop_all(engine)
        engine.dispose()
