from redis import StrictRedis
from config import CACHE_REDIS_HOST, CACHE_REDIS_PORT

redis_client = StrictRedis(CACHE_REDIS_HOST, CACHE_REDIS_PORT,  decode_responses=True)