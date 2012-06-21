# coding=utf-8
import uuid

Sessions = {}

class SessionManager():
    def __init__(self):
        self.sessions = Sessions

    def add(self, session_id, info):
        self.sessions[session_id] = {
            'users': {},
            'msgs': [],
            'info': info,
            }

    def add_user(self, session_id, user_id, is_reply=None):
        if not is_reply: is_reply = 1
        self.sessions[session_id]['users'][user_id] = {
            'unread_msg': [],
            'is_reply': is_reply
        }

    def del_user(self, session_id, user_id):
        del self.sessions[session_id]['users'][user_id]

    def get_session(self, session_id):
        return self.sessions[session_id]['info']

    def is_reply(self, session_id, user_id):
        return self.sessions[session_id][user_id]['is_reply']

    def get_users(self, session_id):
        if self.sessions.has_key(session_id):
            return self.sessions[session_id]['users']
        else:
            return None

    def get_msgs(self, session_id):
        return self.sessions[session_id]['msgs']

    def session_is_exist(self, session_id):
        return self.sessions.has_key(session_id)

    def user_is_exist(self, session_id, user_id):
        return self.sessions[session_id].has_key(user_id)

    def change_unread_clean(self, session_id, user_id, values=None):
        if values:
            self.sessions[session_id]['users'][user_id]['unread_msg'].extend(values)
            #print '#######################',self.sessions[session_id]['users'][user_id]['unread_msg']
        else:
            self.sessions[session_id]['users'][user_id]['unread_msg'] = []


    def get_unread(self, session_id, user_id):
        #print self.sessions[session_id]
        return self.sessions[session_id]['users'][user_id]['unread_msg']

    def get_info(self, session_id):
        return self.sessions[session_id]['info']

    def delete(self, session_id):
        if self.sessions.has_key(session_id):
            del self.sessions[session_id]