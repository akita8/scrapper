"""Contains base model class, with a common interface to the redis db."""
from abc import ABCMeta
from abc import abstractmethod
from redis import StrictRedis

redis_db = StrictRedis()


class BaseModel(metaclass=ABCMeta):
    """Class intended to be inherited."""

    model_type = None

    @abstractmethod
    def create_key(self):
        """It returns the specific key for the model."""

    @classmethod
    def _type(cls):
        return cls.model_type

    def key_exists(self, key):
        """It checks if the hash key is already stored in the right set."""
        return redis_db.sismember(self._type(), key)

    def add_entry(self, values):
        """It adds a new key to the set if it's not present.

        It adds (or updates) the hash to the database.
        """
        key = self.create_key()
        if not self.key_exists(key):
            redis_db.saad(self._type(), key)
        redis_db.hset(key, values)
