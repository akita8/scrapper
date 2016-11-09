"""Module contains base model class and Redis inizialization."""
from abc import ABCMeta
from abc import abstractmethod
from redis import StrictRedis

redis_db = StrictRedis()


class BaseModel(metaclass=ABCMeta):
    """Class intended to be inherited.

    This class is intended as a common interface
    beetween the redis db and the marshmallow schemas.

    Subclasses must override the create key method.
    """

    @abstractmethod
    def key(self):
        """It is expected to be overridden.

        It should return the specific key, needed to operate
        on the hash, as a string of colon separeted values.
        """

    @classmethod
    def key_exists(cls, key):
        """It checks if the hash key is already stored in the right set."""
        return redis_db.sismember(cls.__name__.lower(), key)

    def update(self, values):
        """It adds a new key to the set if it's not present.

        It adds (or updates) the hash to the database.
        """
        key = self.key()
        if not self.key_exists(key):
            redis_db.saad(self._type(), key)
        redis_db.hset(key, values)

    def delete(self):
        """Documentation."""