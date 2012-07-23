# encoding=utf-8
from bchat.core.user import User
from bchat.core.session import Session
from bchat.enum import *


class MsgManager(Session):
    def __init__(self):
        Session.__init__(self)
        self.USER = User()

    def send_notice(self, session_id, notice_type, data, except_id=None, appoint_id=None):
        if not except_id: except_id = []
        if not appoint_id: appoint_id = []

        users_id = self.get_users(session_id)

        data.update({'notice_type': notice_type})
        notice_index = self.add_notice(session_id, data)

        for user_id in users_id:
            is_except_user = not user_id in except_id
            is_appoint_user = (appoint_id == [] and True or (user_id in appoint_id))

            user_is_reply = self.is_reply(session_id, user_id)
            is_reply_message = user_is_reply == MessageIsReplyEnum.reply

            if is_except_user and is_appoint_user and is_reply_message:
                self.add_unread_notice(session_id, user_id, notice_index)
                event = self.USER.get_event(user_id)
                event.set()
                event.clear()

    def send_message(self, session_id, data):
        users_id = self.get_users(session_id)
        message_index = self.add_message(session_id, data)

        for user_id in users_id:
            self.add_unread_message(session_id, user_id, message_index)
            event = self.USER.get_event(user_id)
            event.set()
            event.clear()

    def wait_msg(self, user_id):
        self._get_unread_msgs(user_id)

        if not sessions_msgs:
            self.USER.get_event(user_id).wait(timeout=WAIT_TIMEOUT)
            # event.unlink(self.show)
            self._get_unread_msgs(user_id)

    def _get_unread_msgs(self, user_id):
        sessions_id = self.USER.get_sessions(user_id)

        msgs = []
        for session_id in sessions_id:
            notice_unread_indexs = self.get_unread_notices(session_id, user_id)
            message_unread_indexs = self.get_unread_notices(session_id, user_id)
            if notice_unread_indexs:
            	session_notices = self.get_notices(session_id)
                msgs.extend(
                    self.elect_(lambda x, y: x.append(y), notice_unread_indexs, session_notices))
            if message_unread_indexs:
            	session_messages = self.get_notices(session_id)
                msgs.extend(
                    self.elect_(lambda x, y: x.append(y), message_unread_indexs, session_messages))

        return msgs

    def elect_(function, lst, dct):
        result = []
        for item in lst:
            function(result, dct[item])
        return result






