# coding=utf-8
import time
import datetime
from chat.lib.relativedelta import relativedelta

def current_time(format='%Y-%m-%d %H:%M:%S', **interval):
    if interval:
        obj_time = *time.localtime()[:6]) + relativedelta(**interval)
    else:
        obj_time = *time.localtime()[:6])

    return str(time.strftime(format,
        (datetime.datetime(obj_time).timetuple()))