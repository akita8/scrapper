"""Root conftest."""
import sys
import pytest
import datetime


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


@pytest.fixture(scope='session')
def time():
    """Fixture that returns the same datetime object the entire session."""
    return datetime.datetime.today()


@pytest.fixture(scope='session')
def testing_values(time):
    """Fixuture that returns testing values."""
    return {
        'time': str(time),
        'test1': '1',
        'test2': '1.0',
        'test3': 'test',
        'test4': "[1, 1.0, 'test']"}