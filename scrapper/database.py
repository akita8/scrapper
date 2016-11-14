"""Redis database initialization."""
from redis import StrictRedis

redis_db = StrictRedis(decode_responses=True)
