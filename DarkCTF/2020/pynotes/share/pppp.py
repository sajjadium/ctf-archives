from _note import *

from sys import modules
del modules['os']
keys = list(__builtins__.__dict__.keys())
for k in keys:
    # present for you
    if k not in ['int', 'id', 'print', 'range', 'hex', 'bytearray', 'bytes']:
        del __builtins__.__dict__[k]

/** code **/
