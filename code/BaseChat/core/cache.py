# coding=utf-8
from BaseChat.default import CACHE_EXPIRE
import time, datetime

CacheData = {}

class Cache():
    def __init__(self, expire=None):
        global CACHE_EXPIRE
        if expire:
            CACHE_EXPIRE = expire
        self.cache = CacheData
        self.expire = CACHE_EXPIRE

    def set(self, key, value, expire=None):
        """
        write cache
        """
        begin_time = datetime.datetime(*time.localtime()[:6])
        end_time = begin_time +\
                   datetime.timedelta(seconds=(expire==None and self.expire or expire))
        data = {
            'value': value,
            'begin_time': begin_time,
            'end_time': end_time
        }
        self.cache[key] = data

    def get(self, key):
        """
        read cache
        """
        now_time = datetime.datetime(*time.localtime()[:6])
        if self.cache.has_key(key):
            if self.cache[key]['end_time'] > now_time:
                return self.cache[key]['value']
            else:
                del self.cache[key]
                return None
        else:
            return None

    def remove(self, key):
        """
        delete cache
        """
        if self.cache.has_key(key):
            del self.cache[key]

    def reclock(self, *args):
        """
        relock cache data
        """
        for arg in args:
            value = self.get(arg)
            self.set(arg, value)
