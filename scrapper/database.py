"""Redis database initialization."""
import os
from redis import StrictRedis


if os.getenv('REDIS_TESTING') == 'yes':
    redis_db = StrictRedis(db=1, decode_responses=True)
else:
    redis_db = StrictRedis(decode_responses=True)
print(os.getenv('REDIS_TESTING'))