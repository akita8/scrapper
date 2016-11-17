"""Test module for models package."""
import datetime
import pytest
from scrapper.database import redis_db
from scrapper.models.base import BaseModel


def test_BaseModel_raises_TypeError():
    """It tests that BaseModel can't be instantiated directly."""
    with pytest.raises(TypeError):
        BaseModel()


def test_load_data_new(models, load_state):
    """It tests the models' method load_data."""
    model, values = models
    key, db_flag = load_state
    if db_flag:
        redis_db.hmset(key, values)
        model.load_data(key, from_db=True)
    else:
        model.load_data(values)
    assert isinstance(model.time, datetime.datetime)
    assert isinstance(model.test1, int)
    assert isinstance(model.test2, float)
    assert isinstance(model.test3, str)
    assert isinstance(model.test4, list)


def test_models_update_and_delete(models):
    """It tests the models' methods update and delete."""
    model, values = models
    model.load_data(values)
    model.update()
    key = model.key()
    fields = values.keys()
    keys_ = redis_db.hkeys(key)
    assert redis_db.hgetall(key)
    assert model.key_exists(key)
    for key_ in keys_:
        assert key_ in fields
    model.delete()
    assert not redis_db.hgetall(key)
