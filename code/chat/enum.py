from chat.lib.enum import Enum

UserOnlineStatusEnum = Enum('busy', 'leave', 'online', 'offline')
MessageIsReplyEnum = Enum('reply', 'no_reply')
UserTypeEnum = Enum('administrator', 'user', 'user_b')
MsgTypeEnum = Enum('message', 'inform')