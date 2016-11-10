"""Module contains base model class."""
import datetime
from scrapper.database import redis_db


class BaseModel(object):
    """Class that implements the common model methods.

    It is the application interface to the redis db.
    Subclasses must override the key method making it return
    the correct pattern filled with the proper instance values.
    """

    def __init__(self):
        """It initializes the date variable."""
        self.date = datetime.date.today()

    def key(self):
        """It returns the key needed to operate on the hash."""
        raise NotImplemented

    @classmethod
    def type_(cls):
        """It returns the model type."""
        return cls.__name__.lower()

    def key_exists(self, key):
        """It checks if the hash key is already in the model set in the db."""
        return redis_db.sismember(self.type_(), key)

    def update(self, values):
        """It updates (or creates) the hash data on the redis db.

        It adds a new key to the model set if it's not present.
        """
        key = self.key()
        if not self.key_exists(key):
            redis_db.saad(self.type_(), key)
        redis_db.hmset(key, values)

    def delete(self):
        """It removes the hash key and relative data from the redis db.

        It also removes the key reference in the model set.
        """
        key = self.key()
        redis_db.delete(key)
        redis_db.srem(key)
