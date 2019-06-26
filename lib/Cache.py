#!/usr/bin/env python
import redis

"""
A Redis library
"""
class Cache:

    def __init__(self, host="localhost", port=6379):

        self.host = host
        self.port = port
        self.redis = redis.Redis(host=self.host, port=port)

    def set(self, key, value):
        try:
            self.redis.set(key, value)
        except Exception as err:
            print("Error: Set redis key error", err)
            return None
    def get(self, key):
        try:
            value =  self.redis.get(key).decode()
        except Exception as err:
            print("Warning: No Redis key found", err)
            return 
        return value

    def getkeys(self, keys):
        _keys = []
        for key in self.redis.scan_iter(keys):
            _key=self.redis.get(key).decode()
            _keys.append(_key)
        return _keys

        # delete the key
