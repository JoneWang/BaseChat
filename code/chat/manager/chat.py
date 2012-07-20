import uuid
from bchat.core.user import User
from bchat.core.session import Session
from bchat.enum import *
from bchat.lib import common


class ChatManager():
    def __init__(self):
        self.USER = User()
        self.SESSION = Session()

    def add_user(self, user_id, info, online_status=None):
        if not online_status: online_status = UserOnlineStatusEnum.offline
        self.USER.add(user_id, info, online_status)

    def create_session(self, session_id=None, info=None, creater_id=None):
        if not session_id: session_id = str(uuid.uuid1())
        if not info: info = {'create_time': common.current_time()}
        if user_id:
            info.update({'creater_id': creater_id})
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