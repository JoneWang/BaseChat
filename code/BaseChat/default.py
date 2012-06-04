# coding=utf-8

__author__ = 'JoneWang'

# 默认配置
# core中代码在读取项目settings.py文件时
# 如果未设置某些配置则按此处配置为默认配置

try:
    from settings import CACHE_EXPIRE
except Exception, e:
    CACHE_EXPIRE = 10

try:
    from settings import WAIT_TIMEOUT
except Exception, e:
    WAIT_TIMEOUT = 60