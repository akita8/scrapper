"""Module that contains base model class."""
import abc
from datetime import datetime
from scrapper.database import redis_db
from scrapper.utils import get_logger

logger = get_logger('models')


class BaseModel(metaclass=abc.ABCMeta):
    """Class that implements the common model methods.

    It is the application interface to the redis db.
    Subclasses must override the key method making it return
    the correct pattern filled with the proper instance values.
    """

    def __init__(self):
        """It initializes the datetime variable.

        The variable can be overwritten by load_data method.
        """
        self.time = datetime.today()

    @abc.abstractmethod
    def key(self):
        """Abstract method that has to be overridden."""

    @classmethod
    def type_(cls):
        """Class method that returns the model type."""
        return cls.__name__.lower()

    @classmethod
    def key_exists(cls, key):
        """Method that checks if the hash key is already in the model set."""
        return redis_db.sismember(cls.type_(), key)

    @staticmethod
    def convert(value):
        """Static method that converts strings to the proper type.

        Examples:
        '2016-11-14 11:49:09.0' --> datetime(2016, 11, 14, 11, 49, 9, 0)
        '1.0' --> 1.0
        '1' --> 1.0
        'string' --> 'string'
        """
        datetime_pattern = '%Y-%m-%d %H:%M:%S.%f'
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    try:
                        return datetime.strptime(value, datetime_pattern)
                    except ValueError:
                        return value
        return value

    def load_data(self, data, from_db=False):
        """Method that sets data as instance attributes from either a dict or the db.

        If the flag from_db is set to True the argument data
        should be a string key for the hash in the db.
        """
        if from_db:
            logger.info('Loading data from db hash with key: {}'.format(data))
            data = redis_db.hgetall(data)
        else:
            logger.info('Loading data from dict: {}'.format(data))
        for key, value in data.items():
            value = self.convert(value)
            setattr(self, key, value)

    def update(self):
        """Method that updates (or creates) the hash data on the redis db.

        It adds a new key to the model set if it's not present.
        """
        key = self.key()
        type_ = self.type_()

        logger.info('Updating redis hash: {}'.format(key))
        if not self.key_exists(key):
            info = "Adding the hash key: {} to the redis set {}"
            logger.info(info.format(key, type_))
            redis_db.sadd(type_, key)
        redis_db.hmset(key, self.__dict__)

    def delete(self):
        """Method that removes the hash key and relative data from the redis db.

        It also removes the key reference in the model set.
        """
        key = self.key()
        type_ = self.type_()

        redis_db.delete(key)
        logger.info('Deleting redis hash: {}'.format(key))
        redis_db.srem(self.type_(), key)
        info = "Removing the hash key: {} to the redis set {}"
        logger.info(info.format(key, type_))

    def __repr__(self):
        """Magic methods that returns a printable string of the model."""
        string = '<{}({})>'
        try:
            return string.format(self.type_(), self.key())
        except AttributeError:
            return string.format(self.type_(), 'empty')
