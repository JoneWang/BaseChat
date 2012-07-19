# coding=utf-8
import uuid

def enum(object_name, enum_names):
    object = globals().get(object_name)
    for name in enum_names:
        setattr(object, name, str(uuid.uuid1()))
    return object

class Enum:
    def __init__(self, *arguments):
        print arguments
        idx = 0
        for name in arguments:
            if '=' in name:
                name,val = name.rsplit('=', 1)
                if val.isalnum():
                    idx = eval(val)
            setattr(self, name.strip(), idx)
            idx = idx + 1