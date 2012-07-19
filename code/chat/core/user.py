# coding=utf-8
from gevent.event import Event
from chat.lib.enum import Enum


Users = {}


class UserManagerError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class UserManager():
    def __init__(self):
        self.users = Users
        self.status = Enum('busy', 'leave', 'online', 'offline')
        self.reply_status = Enum('reply', 'no_reply')
        self.type = Enum('administrator', 'user', 'user_b')

    def _get(self, user_id):
        if self.users.has_key(user_id):
            return self.users[user_id]
        else:
            raise UserManagerError, 'User %s not exist' % user_id

    def add(self, user_id, info):
        self.users[user_id] = {
            'status': 0,
            'event': [],
            'sessions': [],
            'info': info,
            }
        self.add_event(user_id)

    def get_info(self, user_id):
        return self._get(user_id)['info']

    def remove(self, user_id):
        del self._get(user_id)

    def is_exist(self, user_id):
        return self.users.has_key(user_id)

    def add_session(self, user_id, session_id):
        self._get(user_id)['sessions'].append(session_id)

    def get_sessions(self, user_id):
        return self._get(user_id)['sessions']

    def remove_session(self, user_id, session_id):
        self._get(user_id)['sessions'].remove(session_id)

    def is_exist_session(self, user_id, session_id):
        return session_id in self.get_sessions(user_id)

    def add_event(self, user_id):
        self._get(user_id)['event'].append(Event())

    def get_event(self, user_id):
        if len(self._get(user_id)['event']) > 1:
            del self._get(user_id)['event'][0: -1]
        return self._get(user_id)['event'][-1]

    def get_status(self, user_id):
        return self._get(user_id)['status']

    def set_status(self, user_id, status):
        self._get(user_id)['status'] = status
