# coding=utf-8
import uuid


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
            'msgs': {'messages': {}, 'notices': {}},
            'info': info,
            }

    def get_info(self, session_id):
        return self._get(session_id)['info']

    def remove(self, session_id):
        del self._get(session_id)

    def add_user(self, session_id, user_id, is_reply):
        self._get(session_id)['users'][user_id] = {
            'unread_msg': {'messages': [], 'notices': []},
            'is_reply': is_reply
        }

    def remove_user(self, session_id, user_id):
        del self._get(session_id)['users'][user_id]

    def is_reply(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['is_reply']

    def get_users(self, session_id):
        return self._get(session_id)['users'].keys()

    def is_exist(self, session_id):
        return self.sessions.has_key(session_id)

    def user_is_exist(self, session_id, user_id):
        return self._get(session_id).has_key(user_id)

    def get_notices(self, session_id):
        return self._get(session_id)['msgs']['notices']

    def get_messages(self, session_id):
        return self._get(session_id)['msgs']['messages']

    def _new_index(self, msgs):
        if len(msgs) > 0:
            index = msgs.keys()[-1] + 1
        else:
            index = 0
        return index

    def add_notice(self, session_id, data):
        index = self._new_index(self.get_notices(session_id))
        self.get_notices(session_id)[index] = data
        return index

    def add_message(self, session_id, data):
        index = self._new_index(self.get_messages(session_id))
        self.get_messages(session_id)[index] = data
        return index

    def add_unread_notice(self, session_id, user_id, index):
        self.get_unread_notices(session_id, user_id).append(index)

    def add_unread_message(self, session_id, user_id, index):
        self.get_unread_messages(session_id, user_id).append(index)

    def get_unread_notices(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['unread_msg']['notices']

    def get_unread_messages(self, session_id, user_id):
        return self._get(session_id)['users'][user_id]['unread_msg']['messages']

    def extend_unread_notices(self, session_id, user_id, indexs):
        self.get_unread_notices(session_id, user_id).extend(values)

    def extend_unread_messages(self, session_id, user_id, indexs):
        self.get_unread_messages(session_id, user_id).extend(values)

    def unread_notices_clean(self, session_id, user_id):
        self.get_unread_notices(session_id, user_id) = []

    def unread_messages_clean(self, session_id, user_id):
        self.get_unread_messages(session_id, user_id) = []