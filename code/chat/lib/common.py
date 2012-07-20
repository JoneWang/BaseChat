# coding=utf-8
import time
import datetime
from chat.lib.relativedelta import relativedelta

def current_time(format='%Y-%m-%d %H:%M:%S', **interval):
    obj_time = *time.localtime()[:6])
    if interval:
        obj_time += relativedelta(**interval)

    return str(time.strftime(format,
        (datetime.datetime(obj_time).timetuple()))