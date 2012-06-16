# coding=utf-8
import copy
import gevent
from core.session import SessionManager
from core.user import UserManager
from core.default import WAIT_TIMEOUT
from settings import WAIT_DELAY

class Busy(): pass;guest_online = Busy()


class MsgType():
    def __init__(self):
        # 用户上线
        self.user_online = 101
        # 用户离线
        self.user_offline = 102

        # 进入会话
        self.session_entry = 301
        # 离开会话
        self.session_leave = 302

        # 聊天消息
        self.message_content = 401
        # 正在输入的消息
        self.message_entering = 402

        # 组织重要关键字设置通知
        self.group_rank_keyword = 501
        # 组织快捷回复设置通知
        self.group_fast_reply = 502

class MsgManager():
    def __init__(self):
        self.type = MsgType()

    def add_msg(self, session_id, data, except_id=None, appoint_id=None):
        """
        将消息添加至列队，并激活长轮询
        """
        #print '----------------- send --------------------'
        #print '----------------- send --------------------'
        #print '----------------- send --------------------', session_id
        #print '----------------- send --------------------', data

        if not except_id: except_id = []
        if not appoint_id: appoint_id = []

        session = SessionManager()

        msgs = session.get_msgs(session_id)
        if len(msgs) > 0:
            index = msgs[-1]['index'] + 1
        else:
            index = 0
        data.update({'index': index})

        msgs.append(data)
        users_id = session.get_users(session_id)
        user = UserManager()

        #print users_id
        for user_id in users_id:
            user_info = users_id[user_id]
            #print user_id, user.get_status(user_id), user_info['is_reply']
            #print user_info
            if ((data['msg_type'] == self.type.message_content and user.get_role(user_id) == user.type.attendant)
                or user.get_status(user_id) != user.status.offline) and not user_id in except_id and (
                appoint_id == [] and True or (user_id in appoint_id)) and (
                (user_info['is_reply'] == user.reply_status.no_reply and data['msg_type'] == self.type.message_content)
                or user_info['is_reply'] == user.reply_status.reply):
                user_info['unread_msg'].append(index)
                event = user.get_event(user_id)
                event.set()
                event.clear()

    def push_all_message(self, session_id, except_id=None, appoint_id=None, index=0):
        if not except_id: except_id = []
        if not appoint_id: appoint_id = []

        user = UserManager()
        session = SessionManager()
        msg = MsgManager()

        users_info = session.get_users(session_id)
        msgs_info = session.get_msgs(session_id)

        msgs_index = []
        for msg_info in msgs_info:
            print msg_info['index']
            if msg_info['index'] > index or index == 0:
                if msg_info['msg_type'] == msg.type.message_content:
                    msgs_index.append(msg_info['index'])

        for user_id in users_info:
            print user.get_user(user_id)['info']['name']
            if not user_id in except_id and (appoint_id == [] and True or (user_id in appoint_id)):
                print '----------------------------------------------------\n--------------------------------------------\n----------------------------------------\n-----------------------------------%s', user_id
                session.change_unread_clean(session_id, user_id, msgs_index)
                event = user.get_event(user_id)
                event.set()
                event.clear()
                #print '########################## all msg'

    def add_msg_to_user(self, session_id, user_id, data):
        pass

    def activate_user_event(self, user_id):
        user = UserManager()
        if user.is_exist(user_id):
            event = user.get_event(user_id)
            event.set()
            event.clear()

    def wait_msg(self, user_id):
        """
        长轮询
        验证未收通知并等待激活
        如果被激活，将用户指定数量的未收通知返回给客户端
        """
        gevent.sleep(WAIT_DELAY)
        user = UserManager()

        sessions_msgs = {}
        self._check_group_msg(sessions_msgs, user_id)
        self._check_session_msg(sessions_msgs, user_id)

        if not sessions_msgs:
            event = user.get_event(user_id)
            event.wait(timeout=WAIT_TIMEOUT)
            #if user.get_status(user_id) != user.status.offline:
            self._check_group_msg(sessions_msgs, user_id)
            self._check_session_msg(sessions_msgs, user_id)

        print ' # # # # # # # # # # # # # # # #', sessions_msgs
        return sessions_msgs

    def _check_session_msg(self, sessions_msgs, user_id):
        """
        验证并读取会话通知
        """
        session = SessionManager()
        user = UserManager()

        sessions_id = user.get_sessions(user_id)

        for session_id in sessions_id:
            unread = session.get_unread(session_id, user_id)
            print session_id, len(unread)
            if len(unread) > 0:
                unread_msgs = session.get_msgs(session_id)
                sessions_msgs[session_id] = self._get_msgs(unread_msgs, unread, user_id)
                session.change_unread_clean(session_id, user_id)

    def _get_msgs(self, msgs, unread, user_id):
        unread_msgs = []
        for msg in msgs:
            if int(msg['index']) in unread:
                msg_bak = copy.copy(msg)
                if msg_bak['msg_type'] == self.type.message_content and msg_bak.has_key('show'):
                    if msg_bak['sender_id'] == user_id:
                        del msg['show']
                unread_msgs.append(msg_bak)
        return unread_msgs

    def _check_group_msg(self, sessions_msgs, user_id):
        """
        验证并读取组织通知
        """
        user = UserManager()
        session = SessionManager()

        group = user.get_group_id(user_id)
        user_info = user.get_user(user_id)
        group_id = user_info['type'] == 'att' and 'KF%s' % group or 'FK%s' % group
        gp_msg = session.get_unread(group_id, user_id)
        if gp_msg:
            sessions_msgs[group_id] = self._get_msgs(session.get_msgs(group_id), gp_msg, user_id)
            session.change_unread_clean(group_id, user_id)

    def _check_user_msg(self, user_id):
        user = UserManager()



