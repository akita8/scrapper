"""Root conftest."""
import sys
import pytest


def pytest_configure(config):
    """Config form 'http://doc.pytest.org/en/latest/example/simple.html'."""
    sys._called_from_test = True


def pytest_unconfigure(config):
    """Config form 'http://doc.pytest.org/en/latest/example/simple.html'."""
    del sys._called_from_test


@pytest.fixture(scope='session')
def db():
    """Fixture that flushes the testing db at the end of the session."""
    from backend.database import redis_db
    yield
    redis_db.flushdb()
