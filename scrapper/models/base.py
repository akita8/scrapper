"""Module contains base model class."""
from datetime import datetime
import logging
import logging.config
from scrapper.database import redis_db
from scrapper.utils import path


logging.config.fileConfig(path('config.ini'))
logger = logging.getLogger('models')


class BaseModel(object):
    """Class that implements the common model methods.

    It is the application interface to the redis db.
    Subclasses must override the key method making it return
    the correct pattern filled with the proper instance values.
    """

    def __init__(self):
        """It initializes the datetime variable.

        The variable can be overwritten by the from_db and from_dict methods.
        """
        self.time = datetime.today()

    def key(self):
        """It returns the key needed to operate on the hash."""
        raise NotImplemented

    @classmethod
    def type_(cls):
        """It returns the model type."""
        return cls.__name__.lower()

    @staticmethod
    def convert(value):
        """It converts strings containing different type of data."""
        datetime_pattern = '%Y-%m-%d %H:%M:%S.%f'
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, datetime_pattern)
            except ValueError:
                if value.isdigit():
                    value = float(value)
        elif isinstance(value, int):
            value = float(value)
        return value

    def load_data(self, data, from_db=False):
        """It sets data as instance attributes from either a dict or the db."""
        if from_db:
            data = redis_db.hgetall(data)
        for key, value in data.items():
            value = self.convert(value)
            setattr(self, key, value)

    def key_exists(self, key):
        """It checks if the hash key is already in the model set in the db."""
        return redis_db.sismember(self.type_(), key)

    def update(self):
        """It updates (or creates) the hash data on the redis db.

        It adds a new key to the model set if it's not present.
        """
        key = self.key()
        if not self.key_exists(key):
            redis_db.sadd(self.type_(), key)
        redis_db.hmset(key, self.__dict__)

    def delete(self):
        """It removes the hash key and relative data from the redis db.

        It also removes the key reference in the model set.
        """
        key = self.key()
        redis_db.delete(key)
        redis_db.srem(self.type_(), key)

    def __repr__(self):
        """Documentation."""
        return '<{}({})>'.format(self.type_(), self.key())
