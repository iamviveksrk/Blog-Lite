from flask_caching import Cache
from redis_client import redis_client
from flask import request
import urllib

cache = Cache()

def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key

def cache_key_feed():
    auth_token = request.headers.get('Authorization')
    key = request.path
    return key

class ClearCache:

    def clear_cache_post(self, post_id):
        key_prefix = f'flask_cache_/post?post_id={post_id}'
        print('redis_client starts with', key_prefix)
        keys = [key for key in redis_client.keys() if key.startswith(key_prefix)]
        print(keys)
        for key in keys:
            print(key)
            redis_client.delete(key)