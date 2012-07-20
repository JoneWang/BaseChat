# coding=utf-8
import uuid
from core.enum import *


Sessions_data = {}


class SessionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Session():
    def __init__(self):
        self.sessions = Sessions_data

    def _get(self, session_id):
        if self.is_exist(session_id):
            return self.users[session_id]
        else:
            raise SessionError, 'Session %s not exist' % session_id

    def add(self, session_id, info):
        self.sessions[session_id] = {
            'users': {},
            'msgs': {'messages': [], 'notices': []},
            'info': info,
            }

    def get_info(self, session_id):
        return self._get(session_id)['info']

    def remove(self, session_id):
        del self._get(session_id)

    def add_user(self, session_id, user_id, is_reply=None):
        if not is_reply: is_reply = MessageIsReplyEnum.reply
        self._get(session_id)['users'][user_id] = {
            'unread_msg': {'messages': [], 'notices': []},
            'is_reply': is_reply
        }

    def del_user(self, session_id, user_id):
        del self._get(session_id)['users'][user_id]

    def get_unread_notices(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['unread_msg']['notices']

    def get_unread_message(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['unread_msg']['messages']

    def is_reply(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['is_reply']

    def get_users(self, session_id):
        return self._get(session_id)['users'].keys()

    def get_notices(self, session_id):
        return self._get(session_id)['msgs']['notices']

    def get_messages(self, session_id):
        return self._get(session_id)['msgs']['messages']

    def is_exist(self, session_id):
        return self.sessions.has_key(session_id)

    def user_is_exist(self, session_id, user_id):
        return self._get(session_id).has_key(user_id)

    def unread_notices_clean(self, session_id, user_id):
        self._get(session_id)['users'][user_id]['unread_msg']['notices'] = []

    def unread_messages_clean(self, session_id, user_id):
        self._get(session_id)['users'][user_id]['unread_msg']['messages'] = []

    def extend_notices(self, session_id, user_id, values):
        self._get(session_id)['users'][user_id]['unread_msg']['notices'].extend(values)

    def extend_messages(self, session_id, user_id, values):
        self._get(session_id)['users'][user_id]['unread_msg']['messages'].extend(values)