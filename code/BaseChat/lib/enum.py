# coding=utf-8
import uuid

def enum(object_name, enum_names):
    object = globals().get(object_name)
    for name in enum_names:
        setattr(object, name, str(uuid.uuid1()))
    return object