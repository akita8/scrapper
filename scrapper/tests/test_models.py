"""Documentation."""
import datetime
import pytest
from scrapper.database import redis_db
from scrapper.models.base import BaseModel
from scrapper.models.current import Stock


now = datetime.datetime.today()
models_params = [
    (Stock(), {'time': str(now), 'symbol': 'test'})
]


@pytest.fixture(params=models_params)
def models(request):
    """Fixture that returns BaseModel instance."""
    return request.param


@pytest.fixture
def db_hash(models):
    """Fixture that adds and then removes a dict to the db for each test."""
    _, values = models
    key = 'test_model'
    redis_db.hmset(key, values)
    yield key
    redis_db.delete(key)


def test_BaseModel_raises_TypeError():
    """It tests that BaseModel can't be instantiated directly."""
    with pytest.raises(TypeError):
        BaseModel()


def test_BaseModel_load_data(models):
    """It tests the BaseModel method load_data with flag 'from_db' false.

    It expects all the item of the dict passed as argument
    to be set as attributes of the instance.
    """
    model, values = models
    model.load_data(values)
    assert isinstance(model.time, datetime.datetime)


def test_BaseModel_load_data_from_db(models, db_hash):
    """It tests the BaseModel method load_data with flag 'from_db' true.

    It expects all the item of the hash in the redis database
    to be set as attributes of the instance.
    """
    model, values = models
    key = db_hash
    model.load_data(key, from_db=True)
    assert isinstance(model.time, datetime.datetime)
