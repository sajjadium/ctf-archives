#!/usr/bin/python3 -u

import auditor
import sys

code = compile(sys.stdin.read(), '<user input>', 'exec')
sys.stdin.close()

for module in set(sys.modules.keys()):
    if module in sys.modules:
        del sys.modules[module]

auditor.activate()
namespace = {}
auditor.exec(code, namespace, namespace)
