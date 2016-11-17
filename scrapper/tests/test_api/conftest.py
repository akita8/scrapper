"""Fixture for api modules."""
import datetime
import pytest
from scrapper.models.current import Stock, Bond


class Parameters:
    """Parameters for fixtures."""

    models = [
        (Stock, {'symbol': 'test_symbol'}),
        (Bond, {'isin': 'test_isin'})]
    load_state = [
        ('', False),
        ('{}:test_load_data', True)]


@pytest.fixture(scope='session')
def time():
    """Fixture that returns the same datetime object the entire session."""
    return datetime.datetime.today()


@pytest.fixture(scope='function', params=Parameters.models)
def models(request, db, time):
    """Fixture that returns the models instances and testing values."""
    testing_values = {
        'time': str(time),
        'test1': '1',
        'test2': '1.0',
        'test3': 'test',
        'test4': "[1, 1.0, 'test']"}
    model, key_values = request.param
    param = (model(), {**key_values, **testing_values})
    return param


@pytest.fixture(scope='function', params=Parameters.load_state)
def load_state(request, time):
    """Fixture to simplify testing the two different uses of load_data."""
    key_pattern, state = request.param
    return (key_pattern.format(time.date()), state)
