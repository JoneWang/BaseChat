# coding=utf-8
import httplib
import json
import time
import md5
import urllib
import uuid
import random
import datetime
import re
from settings import RESULT_TEMPLATE, REQUEST_TIMEOUT

__author__ = 'JoneWang'

def result(*args):
    """
    返回结果格式
    """
    try:
        RESULT_TEMPLATE['error'] = args[0]
        RESULT_TEMPLATE['msg'] = args[1]
        RESULT_TEMPLATE['data'] = args[2]
        return json.dumps(RESULT_TEMPLATE)
    except:
        print ' --- data --- ', args[2]


def get_current_time(format='%Y-%m-%d %H:%M:%S'):
    """
    当前时间
    """
    return str(time.strftime(format, time.localtime(time.time())))


def get_security_key():
    """
    生成密钥
    """
    # 生成一个Population
    pop = [chr(i) for i in xrange(33, 126 + 1)]
    # sample随机选取，然后再Join
    return "".join(random.sample(pop, 64))


def get_auth_key():
    """
    生成授权key
    """
    return str(md5.new(str(uuid.uuid1())).hexdigest())



def http_request(addr, port='80', path='/', params=None, request_method='GET', is_split=False):
    """
    请求server数据
    """
    if is_split:
        conn = httplib.HTTPConnection(addr, port, timeout=REQUEST_TIMEOUT)
        split_length = len(params) / 500
        if len(params) % 500 > 0:
            split_length += 1
        data = '{"error":-1,"msg":"","data":{}}'
        data_id = uuid.uuid1()
        for i in range(split_length):
            for j in range(3):
                params_encode = urllib.urlencode({
                    'data_id': data_id,
                    'data': params[i * 500:(i + 1) * 500],
                    'index': i,
                    'is_end': i == (split_length - 1) and 1 or 0
                })
                conn.request('GET', path + '?%s' % params_encode)
                result = conn.getresponse()
                data = result.read()
                json_data = json.loads(data)
                if i == (split_length - 1) or not json_data['error']:
                    break
        conn.close()
    else:
        conn = httplib.HTTPConnection(addr, port, REQUEST_TIMEOUT)
        if params:
            params_encode = urllib.urlencode(params)
            conn.request(request_method, path + '?%s' % params_encode)
            #print addr + '/' + path + '?%s' % params_encode
        else:
            params_encode = None
            conn.request('GET', path)
        result = conn.getresponse()
        data = result.read()
        conn.close()

    return json.loads(data)


def join_ids(id1, id2):
    """
    拼接id
    """
    if id1 > id2:
        id = ''.join([id1, id2])
    else:
        id = ''.join([id2, id1])
    return id


class Test():
    def __init__(self):
        self.begin_time = datetime.datetime(*time.localtime()[:6])


    def print_time(self, index):
        now = datetime.datetime(*time.localtime()[:6])
        print '####################################', '----', index, '----', self.timediff(self.begin_time, now)

    def timediff(self, timestart, timestop):
        t = (timestop - timestart)
        time_day = t.days * 24 * 60 * 60
        s_time = t.seconds
        ms_time = t.microseconds / 1000000
        usedtime = int(s_time + ms_time)
        time_hour = usedtime / 60 / 60
        time_minute = (usedtime - time_hour * 3600 ) / 60
        time_second = usedtime - time_hour * 3600 - time_minute * 60
        time_micsecond = (t.microseconds - t.microseconds / 1000000) / 1000

        retstr = "%d天%d小时%d分%d秒%d毫秒" % (time_day, time_hour, time_minute, time_second, time_micsecond)
        return retstr


def contains(seq, aset):
    if type(seq) != unicode: seq = seq.decode('utf-8')
    if type(aset) != unicode: aset = aset.decode('utf-8')
    return bool(re.search(seq, aset, re.IGNORECASE))