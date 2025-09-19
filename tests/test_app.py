import pytest
import sys
import os
import tempfile


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app, db, Users, is_money_format


@pytest.mark.parametrize("value, expected", [
    ("100", True),
    ("-50", True),
    ("20.50", True),
    ("20.123", False),
    ("abc", False),
])
def test_is_money_format(value, expected):
    assert is_money_format(value) == expected


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{db_path}"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"check_same_thread": False}}

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        with app.app_context():
            db.drop_all()
        os.unlink(db_path)



def test_signup_creates_user(client):
    response = client.post("/signup/", data={
        "username": "newuser",
        "password": "password123",
        "income": "1000",
        "goal": "500"
    }, follow_redirects=True)

    assert b"Account successfully created!" in response.data
    with app.app_context():
        user = Users.query.filter_by(username="newuser").first()
        assert user is not None

def test_login_wrong_password(client):
    with app.app_context():
        user = Users(username="tester", password="secret")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login/", data={
        "username": "tester",
        "password": "wrongpass"
    }, follow_redirects=True)

    assert b"Login failed" in response.data

def test_login_and_session(client):
    with app.app_context():
        user = Users(username="tester", password="secret")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login/", data={
        "username": "tester",
        "password": "secret"
    }, follow_redirects=True)

    assert b"information" in response.data.lower()  # redirected to info page

def test_add_event(client):
    # First signup + login
    client.post("/signup/", data={
        "username": "eventuser",
        "password": "pass",
        "income": "500",
        "goal": "1000"
    })
    client.post("/login/", data={"username": "eventuser", "password": "pass"})

    # Add event
    response = client.post("/calendar/add-event/15-8-2025/", data={
        "event-name": "Test Event",
        "event-type": "work",
        "event-transaction": "200",
        "event-description": "Bonus payment"
    }, follow_redirects=True)

    assert b"calendar" in response.data
    with app.app_context():
        user = Users.query.filter_by(username="eventuser").first()
        assert "15-8-2025" in user.events