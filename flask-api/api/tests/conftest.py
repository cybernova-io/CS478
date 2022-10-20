import os
import pytest
import tempfile

from api import create_app, db as _db

class TestConfig:

    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = False
    DEBUG = True



@pytest.fixture(scope="session")
def app(request):
    """Test session-wide test `Flask` application."""
    app = create_app(TestConfig)
    return app


@pytest.fixture(autouse=True)
def _setup_app_context_for_test(request, app):
    """
    Given app is session-wide, sets up a app context per test to ensure that
    app and request stack is not shared between tests.
    """
    ctx = app.app_context()
    ctx.push()
    yield  # tests will run here
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    """Returns session-wide initialized database"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope="function")
def session(app, db, request):
    """Creates a new database session for each test, rolling back changes afterwards"""
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    _db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()