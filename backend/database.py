"""Redis database initialization."""
import sys
from redis import StrictRedis

if hasattr(sys, '_called_from_test'):
    redis_db = StrictRedis(db=10, decode_responses=True)
else:
    redis_db = StrictRedis(decode_responses=True)

