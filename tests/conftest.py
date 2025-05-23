import pytest
from fastapi.testclient import TestClient
from _24hi25back.app.application import create_application
from _24hi25back.app.db.session import engine, SessionLocal
from _24hi25back.app.db.base import Base
from _24hi25back.app.db.models import AuthUser
@pytest.fixture
def test_client():
    app = create_application()
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def create_auth_users(db_session):
    active_superuser = AuthUser.create_user(username="active_superuser",
                                            password="123456",
                                            is_superuser=True)
    inactive_superuser = AuthUser.create_user(username="inactive_superuser",
                                              password="123456",
                                              is_superuser=True,
                                              is_active=False)
    active_user = AuthUser.create_user(username="active_user",
                                       password="654321")
    inactive_user = AuthUser.create_user(username="inactive_user",
                                         password="654321",
                                         is_active=False)
    users = dict(active_superuser=active_superuser,
                 inactive_superuser=inactive_superuser,
                 active_user=active_user,
                 inactive_user=inactive_user)
    db_session.add_all(users.values())
    db_session.commit()

    usernames = db_session.query(AuthUser).with_entities(AuthUser.username).all()
    usernames = {u[0] for u in usernames}
    assert usernames.intersection(users.keys()) == set(users.keys())
    yield users, db_session
