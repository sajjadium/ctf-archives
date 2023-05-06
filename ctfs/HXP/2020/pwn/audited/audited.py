#!/usr/bin/python3 -u

import sys
from os import _exit as __exit

def audit(name, args):
    if not audit.did_exec and name == 'exec':
        audit.did_exec = True
    else:
        __exit(1)
audit.did_exec = False

sys.stdout.write('> ')
try:
    code = compile(sys.stdin.read(), '<user input>', 'exec')
except:
    __exit(1)
sys.stdin.close()

for module in set(sys.modules.keys()):
    if module in sys.modules:
        del sys.modules[module]

sys.addaudithook(audit)

namespace = {}
try:
    exec(code, namespace, namespace)
except:
    __exit(1)
__exit(0)
