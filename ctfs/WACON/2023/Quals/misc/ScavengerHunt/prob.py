#!/usr/bin/env python3

import secret
import pyseccomp
import sys

print("Find the treasure!")
data = input()

f = pyseccomp.SyscallFilter(defaction=pyseccomp.KILL)
f.add_rule(pyseccomp.ALLOW, 'rt_sigaction')
f.add_rule(pyseccomp.ALLOW, 'munmap')
f.add_rule(pyseccomp.ALLOW, 'exit_group')
f.add_rule(pyseccomp.ALLOW, 'exit')
f.add_rule(pyseccomp.ALLOW, 'brk')
f.load()
del pyseccomp
del f
del sys

__builtins__ = {}
try:
    eval(data, {'__builtins__': {}}, {'__builtins__': {}})
except:
    pass
exit(0)
