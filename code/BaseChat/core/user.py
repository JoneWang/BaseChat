# coding=utf-8
from gevent.event import Event

Users = {}


class Busy(): pass;busy = Busy()


class Leave(): pass;leave = Leave()


class Online(): pass;online = Online()


class Offline(): pass;offline = Offline()


class Reply(): pass;reply = Reply()


class NoReply(): pass;no_reply = NoReply()


class UserStatus():
    def __init__(self):
        self.busy = busy
        self.leave = leave
        self.online = online
        self.offline = offline


class ReplyStatus():
    def __init__(self):
        self.reply = reply
        self.no_reply = no_reply


class UserType():
    def __init__(self):
        pass


class UserManager():
    def __init__(self):
        self.users = Users
        self.status = UserStatus()
        self.reply_status = ReplyStatus()
        self.type = UserType()

    def add(self, user_id, info):
        self.users[user_id] = {
            'status': 0,
            'event': [Event()],
            'sessions': [],
            'info': info,
            }

    def add_session(self, user_id, session_id):
        self.users[user_id]['sessions'].append(session_id)

    def remove_session(self, user_id, session_id):
        self.users[user_id]['sessions'].remove(session_id)

    def get_sessions(self, user_id):
        return self.users[user_id]['sessions']

    def get_user(self, user_id):
        if self.users.has_key(user_id):
            return self.users[user_id]['info']
        else:
            return None

    def is_exist(self, user_id):
        return self.users.has_key(user_id)

    def is_exist_session(self, user_id, session_id):
        return session_id in self.get_sessions(user_id)

    def get_event(self, user_id):
        if len(self.users[user_id]['event']) > 1:
            del self.users[user_id]['event'][0]
        return self.users[user_id]['event'][-1]

    def add_event(self, user_id):
        self.users[user_id]['event'].append(Event())

    def get_status(self, user_id):
        """
        获取用户状态
        """
        if self.users.has_key(user_id):
            return self.users[user_id]['status']
        else:
            return self.status.offline

    def set_status(self, user_id, status):
        self.users[user_id]['status'] = status

    def delete(self, user_id):
        if self.users.has_key(user_id):
            del self.users[user_id]
