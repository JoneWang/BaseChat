# coding=utf-8

# default setting

try:
    from settings import CACHE_EXPIRE
except Exception, e:
    CACHE_EXPIRE = 10

try:
    from settings import WAIT_TIMEOUT
except Exception, e:
    WAIT_TIMEOUT = 60