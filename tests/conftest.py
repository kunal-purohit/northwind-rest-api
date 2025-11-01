import pytest
from app import create_app
from app.database import db


@pytest.fixture(scope="session")
def app():
    app = create_app("test")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
