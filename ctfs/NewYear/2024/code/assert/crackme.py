# uncompyle6 version 3.5.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: crackme.py
# Compiled at: 2011-09-19 04:54:37
import sys, types
assert len(sys.argv) == 10
a, b, c, d, e, f, g, h, i = [ int(x) for x in sys.argv[1:] ]
assert b == c
assert c == g
assert g == h
assert g + b + c == 0
codestr = ('').join(chr(x) for x in [a, b, c, d, e, f, g, h, i])
result = ''
assert 3 * a + 12 * d + e + 4 * f + 6 * i == 2194
assert -6 * a + 2 * d - 4 * e - f + 9 * i == -243
assert a + 6 * d + 2 * e + 7 * f + 11 * i == 2307
assert 5 * a - 2 * d - 7 * e + 76 * f + 8 * i == 8238
assert 2 * a - 2 * d - 2 * e - 2 * f + 2 * i == -72

def xorc(a, b):
    return chr(ord(a) ^ ord(b))


def xorstr(a, b):
    return ('').join([ xorc(a[(i % len(a))], c) for i, c in enumerate(b) ])


result += xorstr(codestr, '\x1bro#&\x0b{t;\x19_44;Wrt\x0cLp35|\x100r\x0c\x15s_1{\x16y_&\x0f3f2$;wh`\x12_dt*\x11gg:\x12g_7:Tgrg\x11s}')

def getSolutionAsParameterAndPrint(myChallengeSolution):
    print (0)


recycled_code = getSolutionAsParameterAndPrint.func_code
new_code = types.CodeType(recycled_code.co_argcount, recycled_code.co_nlocals, recycled_code.co_stacksize, recycled_code.co_flags, codestr, recycled_code.co_consts, recycled_code.co_names, recycled_code.co_varnames, recycled_code.co_filename, recycled_code.co_name, recycled_code.co_firstlineno, recycled_code.co_lnotab, recycled_code.co_freevars, recycled_code.co_cellvars)
new_fun = types.FunctionType(new_code, globals(), 'keepOnDigging', getSolutionAsParameterAndPrint.func_defaults)
new_fun(result)