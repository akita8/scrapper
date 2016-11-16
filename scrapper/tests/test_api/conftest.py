"""Fixture for api modules."""
import datetime
import pytest
from scrapper.models.current import Stock, Bond


@pytest.fixture(scope='session')
def time():
    """Fixture that returns the same datetime object the entire session."""
    return datetime.datetime.today()


@pytest.fixture(scope='function', params=[(Stock, {'symbol': 'test_symbol'}),
                                          (Bond, {'isin': 'test_isin'})])
def models(request, db, time):
    """Fixture that returns the models instances and testing values."""
    testing_values = {
        'time': str(time),
        'test1': '1',
        'test2': '1.0',
        'test3': 'test'}
    param = (request.param[0](), {**request.param[1], **testing_values})
    return param
