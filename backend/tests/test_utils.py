"""Tests for utils module."""
from datetime import datetime
from backend.utils import convert


def test_BaseModel_convert(testing_values):
    """It tests the BaseModel static method convert."""
    assert isinstance(convert(testing_values['time']), datetime)
    assert isinstance(convert(testing_values['test1']), int)
    assert isinstance(convert(testing_values['test2']), float)
    assert isinstance(convert(testing_values['test3']), str)
    assert isinstance(convert(testing_values['test4']), list)