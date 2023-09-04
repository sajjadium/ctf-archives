#!/usr/bin/python3
# Heavily based on AZ's you shall not call (ictf 2023), because that was a great chall 

import __main__

# Security measure -- don't let people get io module
from io import BytesIO

from my_pickle import _Unpickler as Unpickler

class mgk:
    class nested:
        pass


mgk.nested.__import__ = __import__
mgk.nested.banned = list(Unpickler.__dict__.keys())
E = type('', (), {'__eq__': lambda s,o:o})() # from hsctf 2023
x = vars(object) == E
x['mgk'] = mgk
del x
del mgk
del E

def __setattr__(self, a, b):  # wow look it's the custom setattr no one asked for!!!!
    if a not in object.mgk.nested.banned:
        __main__ = object.mgk.nested.__import__('__main__')
        if not ((a == 'setattr' or '__' in a) and self == __main__): # overwriting my protections? How dare you!
            try:
                object.__setattr__(self, a, b)
            except:
                type.__setattr__(self, a, b)

Unpickler.__setattr__ = __setattr__
__import__('builtins').__dict__['setattr'] = __setattr__
del __setattr__


def __import__(x, *_): # ok who needs more than 1 arg like wtf i did not know there was 5 args lmfao
    if x in ['builtins', '__main__']:
        return object.mgk.nested.__import__(x) # this is fair trust
__import__('builtins').__dict__['__import__'] = __import__
del __main__.__import__


E = type('', (), {'__eq__': lambda s,o:o})()
x = vars(type(__main__)) == E
def mgetattr(self, a, d=None):
    for x in ['exe', 'os', 'break', 'eva', 'help', 'sys', 'load', 'open', 'dis', 'lic', 'cre']:
        if x in a:
            return None
    else:
        try:
            return object.__getattribute__(self, a)
        except:
            try:
                return type.__getattribute__(self, a)
            except:
                return d

x['__getattribute__'] = mgetattr # not paranoid
__import__('builtins').__dict__['getattr'] = mgetattr # :>

del E
del x
del __main__.mgetattr

# Security measure -- remove dangerous magic
for k in list(globals()):
    if '_' in k and k not in ['__main__', '__builtins__']:
        del globals()[k]
del k


# Security measure -- remove dangerous magic
__builtins__ = vars(__builtins__)
for x in ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__build_class__', '__debug__', '__import__']:
    del __builtins__[x]

try:
    up = Unpickler(BytesIO(bytes.fromhex(input(">>> "))))
    up.load()
except:
    pass