"""Base model class."""
import abc
from ast import literal_eval
from datetime import datetime
from scrapper.database import redis_db
from scrapper.utils import get_logger

logger = get_logger('models')


class BaseModel(metaclass=abc.ABCMeta):
    """Class that implements the common model methods.

    It is the application main interface to the redis db.
    Subclasses must override the key method making it return
    the correct key pattern filled with the proper instance values.
    """

    def __init__(self):
        """It initializes the datetime variable.

        The variable can be overwritten by the load_data method.
        """
        self.time = datetime.today()

    @abc.abstractmethod
    def key(self):
        """Abstract method that has to be overridden."""

    @property
    def model_type(self):
        """Method that returns the model type."""
        return self.__class__.__name__.lower()

    def key_exists(self):
        """Method for checking if model key already exists in db."""
        return redis_db.sismember(self.model_type, self.key())

    def get_model_keys(self):
        """Method that returns the keys stored in the model set."""
        return redis_db.smembers(self.model_type)

    @staticmethod
    def convert(value, datetime_pattern='%Y-%m-%d %H:%M:%S.%f'):
        """Static method that converts strings to the proper type.

        Examples:
        '2016-11-14 11:49:09.0' --> datetime(2016, 11, 14, 11, 49, 9, 0)
        '1.0' --> 1.0
        '1' --> 1.0
        'string' --> 'string'
        "[1, 1.0, 'string']" --> [1, 1.0, 'string']
        """
        try:
            return literal_eval(value)
        except (ValueError, SyntaxError):
            if isinstance(value, str):
                try:
                    return datetime.strptime(value, datetime_pattern)
                except ValueError:
                    return value
            else:
                return value

    def from_db(self, key=None, many=False):
        """Method populates the model with data from the redis db."""
        if many:
            keys = self.get_model_keys()
            models = []
            for key in keys:
                m = self.__class__().from_db(key)
                models.append(m)
            return models
        else:
            data = redis_db.hgetall(key)
            if data:
                return self.from_dict(data)
            else:
                raise KeyError("{} doesn't exist in the database".format(data))

    def from_dict(self, data):
        """Method populates the model with data from a pyton dict."""
        self.__dict__ = {key: self.convert(val) for key, val in data.items()}
        return self

    def update(self):
        """Method that updates (or creates) the hash data on the redis db.

        It adds a new key to the model's set if it's not present.
        """
        if not self.key_exists():
            redis_db.sadd(self.model_type, self.key())
            info = "Hash key {} added to the redis set {}"
            logger.info(info.format(self.key(), self.model_type))
        redis_db.hmset(self.key(), self.__dict__)
        logger.info('Redis hash with key {} updated'.format(self.key()))

    def delete(self):
        """Method that removes the hash key and relative data from the redis db.

        It also removes the key reference in the model set.
        """
        redis_db.delete(self.key())
        logger.info('Redis hash {} deleted'.format(self.key()))
        redis_db.srem(self.model_type, self.key())
        info = "Hash key {} removed from the redis set {}"
        logger.info(info.format(self.key(), self.model_type))
