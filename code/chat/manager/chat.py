# encoding=utf-8
import uuid
from bchat.core.user import User
from bchat.core.session import Session
from bchat.enum import *
from bchat.lib import common

from gevent.event import Event


class ChatManager():
    def __init__(self):
        self.USER = User()
        self.SESSION = Session()

    def add_user(self, user_id, info, online_status=None):
        if not online_status: online_status = UserOnlineStatusEnum.offline
        self.USER.add(user_id, info, online_status)
        self.USER.add_event(user_id, Event())

    def create_session(self, info, session_id=None):
        if not session_id: session_id = str(uuid.uuid1())
        self.SESSION.add(session_id, info)
        return session_id

    def entry_session(self, session_id, user_id, is_reply=None):
        if not is_reply: is_reply = MessageIsReplyEnum.reply
        self.USER.add_session(user_id, session_id)
        self.SESSION.add_user(session_id, user_id, is_reply)

    def leave_session(self, user_id, session_id):
        self.USER.remove_session(user_id, session_id)
        self.SESSION.remove_user(session_id, user_id)

    def remove_session(self, session_id):
        self.SESSION.remove(session_id)