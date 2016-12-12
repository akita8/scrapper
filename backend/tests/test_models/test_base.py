"""Tests for base module of models package."""
import pytest
from backend.database import redis_db
from backend.models.base import BaseModel


def test_BaseModel_raises_TypeError():
    """It tests that BaseModel can't be instantiated directly."""
    with pytest.raises(TypeError):
        BaseModel()


def test_models_from_db(models, time):
    """It tests the models' method from db."""
    model, values, key = models
    redis_db.hmset(key, values)
    model.from_db(key)
    assert hasattr(model, 'time')
    assert hasattr(model, 'test1')
    assert hasattr(model, 'test2')
    assert hasattr(model, 'test3')
    assert hasattr(model, 'test4')


def test_models_from_db_many(models):
    """It tests the models' method from db with flag many."""
    # sbagliato da mettere a posto range for
    model, values, key = models
    expected = [i for i in range(5)]
    for j in range(5):
        values['test_many'] = j
        key = '{}{}'.format(key, j)
        redis_db.hmset(key, values)
    collection = model.from_db(many=True)
    for k, m in enumerate(collection):
        assert m.test_many == expected[k]
        assert isinstance(m.test_many, int)


def test_models_update_and_delete(models):
    """It tests the models' methods update and delete."""
    model, values, key = models
    model.from_dict(values)
    model.update_db()
    fields = values.keys()
    hash_keys = redis_db.hkeys(model.key())
    assert redis_db.hgetall(key)
    for key in hash_keys:
        assert key in fields
    model.delete()
    assert not redis_db.hgetall(model.key())
