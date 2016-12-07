"""Fixtures for testing models."""
import pytest
from backend.models.current import Stock, Bond


class Parameters:
    """Parameters for fixtures."""

    models = [
        # model  dict of key attributes     key pattern
        (Stock, {'symbol': 'test_symbol'}, '{}:test_symbol'),
        (Bond, {'isin': 'test_isin'}, '{}:test_isin')]


@pytest.fixture(scope='function', params=Parameters.models)
def models(request, time, testing_values):
    """Fixture that returns the models instances and testing values."""
    model, key_values, key_pattern = request.param
    key = key_pattern.format(time.date())
    param = (model(), {**key_values, **testing_values}, key)
    return param
