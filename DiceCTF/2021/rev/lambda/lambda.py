#!/usr/bin/env python3

import sys
sys.setrecursionlimit(3000)

# -----
# This section is just used to implement tail-recursion.
# You probably don't need to reverse this but you can try if you want ;p
class TR(Exception):
    SEEN = []
    
    def __init__(self, key, args, kwargs):
        self.key = key
        self.args = args
        self.kwargs = kwargs

def T(fn, name=''):
    def _fn(*args, **kwargs):
        key = id(_fn)
        if key in TR.SEEN:
            raise TR(key, args, kwargs)
        else:
            TR.SEEN.append(key)
            while True:
                try:
                    val = fn(*args, **kwargs)
                    TR.SEEN = TR.SEEN[:TR.SEEN.index(key)]
                    return val
                except TR as e:
                    if e.key != key:
                        raise
                    else:
                        args = e.args
                        kwargs = e.kwargs
                        
                    TR.SEEN = TR.SEEN[:TR.SEEN.index(key)+1]

    return _fn

# -----
# Sice machine:

____=lambda _:lambda __,**___:_(*__,**___)
_____=____(lambda _,*__:_)
______=____(lambda _,*__:__)
_______=____(lambda _,__:_)
________=____(lambda _,__:__)
_________=lambda *_:_
__________=lambda _,__,___:_____(______(_________(*(((),)*(_==())),___,__)))()
___________=lambda _:(_,)
____________=____(lambda *_,___=():__________(_,lambda:____________(______(_),___=___________(___)),lambda:___))
_____________=____(lambda *_:_________(*______(_),_____(_)))
______________=lambda _,__,___:__________(_,lambda:______________(_____(_),___(__),___),lambda:__)
_______________=T(lambda _,__,___:__________(_,lambda:_______________(_____(_),___(__),___),lambda:__))
________________=____(lambda *_:_______________(_____(____________(_)),_,_____________))
_________________=____(lambda *_:__________(______(_),lambda:_________________(_________(___________(_____(_)),*______(______(_)))),lambda:___________(_____(_))))
__________________=lambda _:_______________(_,0,lambda __:__+1)
___________________=lambda _,__,___:__________(_,lambda:___________________(______(_),__,_________(*___,__(_____(_)))),lambda:___)
____________________=lambda _,__:___________________(_,__,())
_____________________=lambda _,__,___:(__________(_______(_____(__)),lambda:__________(_______(_______(_____(__))),lambda:((_________(_____(___),*______(_)),_____________(__),______(___))),lambda:((_,_____________(__),_________(_____(_),*___)))),lambda:__________(_______(________(_____(__))),lambda:__________(_______(_______(________(_____(__)))),lambda:((______________(_____(___),_,_____________),_____________(__),______(___))),lambda:((______________(_____(___),_,________________),_____________(__),______(___))),),lambda:__________(_______(________(________(_____(__)))),lambda:__________(_______(_______(________(________(_____(__))))),lambda:(_,______________(_____(_______(_______(________(________(_____(__)))))),__,________________),___),lambda:(_,______________(_____(________(_______(________(________(_____(__)))))),__,_____________),___)),lambda:__________(_______(________(________(________(_____(__))))),lambda:__________(_______(_______(________(________(________(_____(__)))))),lambda:(_,_____________(__),_________(_____(_______(_______(________(________(________(_____(__))))))),*___)),lambda:(_,_____________(__),_________(_____(_______________(_____(________(_______(________(________(________(_____(__))))))),___,_____________)),*___))),lambda:__________(_______(________(________(________(________(_____(__)))))),lambda:__________(_______(_______(________(________(________(________(_____(__))))))),lambda:(_,__________(_____(___),lambda:_____________(__),lambda:_____________(_____________(__))),______(___)),lambda:(_,______________(_____(___),__,_____________),______(___))),lambda:__________(_______(________(________(________(________(________(_____(__))))))),lambda:__________(_______(_______(________(________(________(________(________(_____(__)))))))),lambda:(_,_____________(__),_________(_______________(_____(___),_____(______(___)),___________),*______(______(___)))),lambda:(_,_____________(__),_________(_______________(_____(___),_____(______(___)),_____),*______(______(___))))),lambda:())))))))
______________________=T(lambda _,__,___:__________(_____(__),lambda:______________________(*_____________________(_,__,___)),lambda:_))
_______________________=lambda _,__:____________________(______________________(((),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),()),__,_________(*____________________(____________________(_,lambda _:((),)*_),_________________),*(((),(),(),(),(),(),(),(),(),(),(),(),(),(),(),())))),__________________)

# -----

def load(cs, i=0):
    objs = []
    while True:
        if cs[i+1] == ')':
            return tuple(objs), i+1
        elif cs[i+1] == '(':
            obj, i = load(cs, i+1)
            objs.append(obj)
        elif cs[i+1] == ',':
            i += 1

# this is apparently "too nested" for the native python parser, so we need to use a custom parser
prog_string = open('./prog', 'r').read()
prog, _ = load(prog_string)

flag = input('flag plz: ').encode('ascii')
print('checking...')

# --- takes 1-2 minutes to check flag
o = _______________________(flag, prog)
# ---

output = bytes(o[:o.index(0)]).decode('ascii')
print(output)

if output == b'Correct!':
    print('Flag: %s' % flag)
