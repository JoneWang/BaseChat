# coding=utf-8


Users_data = {}


class UserError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class User():
    def __init__(self):
        self.users = Users_data

    def _get(self, user_id):
        if self.is_exist(user_id):
            return self.users[user_id]
        else:
            raise UserManagerError, 'User %s not exist' % user_id

    def add(self, user_id, info, online_status):
        self.users[user_id] = {
            'status': online_status,
            'event': [],
            'sessions': [],
            'info': info,
            }

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

    def session_is_exist(self, user_id, session_id):
        return session_id in self.get_sessions(user_id)

    def add_event(self, user_id, Event):
        self._get(user_id)['event'].append(Event)

    def get_event(self, user_id):
        if len(self._get(user_id)['event']) > 2:
            del self._get(user_id)['event'][0: -1]
        return self._get(user_id)['event'][-1]

    def get_status(self, user_id):
        return self._get(user_id)['status']

    def set_status(self, user_id, status):
        self._get(user_id)['status'] = status
