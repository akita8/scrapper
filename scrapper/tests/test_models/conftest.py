"""Fixture for api modules."""
import datetime
import pytest
from scrapper.models.current import Stock, Bond


class Parameters:
    """Parameters for fixtures."""

    models = [
        # model  dict of key attributes     key pattern
        (Stock, {'symbol': 'test_symbol'}, '{}:test_symbol'),
        (Bond, {'isin': 'test_isin'}, '{}:test_isin')]


@pytest.fixture
def testing_values():
    """Fixuture that returns testing values."""
    return {
        'time': str(datetime.datetime.today()),
        'test1': '1',
        'test2': '1.0',
        'test3': 'test',
        'test4': "[1, 1.0, 'test']"}


@pytest.fixture(scope='session')
def time():
    """Fixture that returns the same datetime object the entire session."""
    return datetime.datetime.today()


@pytest.fixture(scope='function', params=Parameters.models)
def models(request, time, testing_values):
    """Fixture that returns the models instances and testing values."""
    testing_values['time'] = str(time)
    model, key_values, key_pattern = request.param
    key = key_pattern.format(time.date())
    param = (model(), {**key_values, **testing_values}, key)
    return param
