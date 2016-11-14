"""Documentation."""
import datetime
import pytest
from scrapper.database import redis_db
from scrapper.models.base import BaseModel


@pytest.fixture(scope='module')
def values():
    """Fixture that returns a basic testing dict."""
    now = datetime.datetime.today()
    return {'time': now, 'test1': 1, 'test2': '2', 'test3': 'test'}


@pytest.fixture
def basemodel():
    """Fixture that returns BaseModel instance."""
    return BaseModel()


@pytest.fixture
def db_hash(request, values):
    """Fixture that adds and then removesa a dict to the db for each test."""
    values['time'] = str(values['time'])
    print(values['time'])
    key = 'test_basemodel'
    redis_db.hmset(key, values)

    def tear_down():
        redis_db.delete(key)
    request.addfinalizer(tear_down)
    return key


def test_BaseModel_load_data(basemodel, values):
    """It tests the BaseModel method load_data with flag 'from_db' false.

    It expects all the item of the dict passed as argument
    to be set as attributes of the instance.
    """
    basemodel.load_data(values)
    assert isinstance(basemodel.time, datetime.datetime)
    assert isinstance(basemodel.test1, float)
    assert isinstance(basemodel.test2, float)
    assert isinstance(basemodel.test3, str)


def test_BaseModel_load_data_from_db(basemodel, db_hash):
    """It tests the BaseModel method load_data with flag 'from_db' true.

    It expects all the item of the hash in the redis database
    to be set as attributes of the instance.
    """
    key = db_hash
    basemodel.load_data(key, from_db=True)
    assert isinstance(basemodel.time, datetime.datetime)
    assert isinstance(basemodel.test1, float)
    assert isinstance(basemodel.test2, float)
    assert isinstance(basemodel.test3, str)
