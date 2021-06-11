#!/usr/bin/env python2.7
from sys import modules
del modules['os']
del modules['sys']
del modules
keys = list(__builtins__.__dict__.keys())

EVAL = eval
LEN = len
RAW_INPUT = raw_input
TRUE = True
FALSE = False
TYPE = type
INT = int

for k in keys:
    if k not in ['False', 'None', 'True', 'bool', 'bytearray', 'bytes', 'chr', 'dict', 'eval', 'exit', 'filter', 'float', 'hash', 'int', 'iter', 'len', 'list', 'long', 'map', 'max', 'ord', 'print', 'range', 'raw_input', 'reduce', 'repr', 'setattr', 'sum', 'type']:
        del __builtins__.__dict__[k]

def print_eval_result(x):
    if TYPE(x) != INT:
        print('wrong program')
        return
    print(x)

def check_eval_str(s):
    s = s.lower()
    if LEN(s) > 0x1000:
        return FALSE
    for x in ['eval', 'exec', '__', 'module', 'class', 'globals', 'os', 'import']:
        if x in s:
            return FALSE
    return TRUE

def sandboxed_eval(s):
    print_eval_result = None
    check_eval_str = None
    sandboxed_eval = None
    evaluator = None
    return EVAL(s)

def evaluator():
    print('Welcome to yet yet another sandboxed python evaluator!')
    print('Give me an expression (ex: 1+2): ')
    s = RAW_INPUT('> ').lower()
    if check_eval_str(s):
        print_eval_result(sandboxed_eval(s))
    else:
        print('Invalid input')
evaluator()
