#!/usr/bin/env python
import re
import sys


class Nobuffers:
    def __init__(self, stream, limit=1024):
        self.stream = stream
        self.limit = limit

    def write(self, data):
        if len(data) > self.limit:
            raise ValueError(f"Data exceeds the maximum limit of {self.limit} characters")
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        datas = [f"{data}\n" for data in datas if len(data) <= self.limit]
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


blacklisted_chars = re.escape('\\(~}?>{)&/%`<$|*=#!-@+"\'0123456789;')
blacklisted_words = [
    'unicode', 'name', 'setattr', 'import', 'open', 'enum',
    'char', 'quit', 'getattr', 'locals', 'globals', 'len',
    'exit', 'exec', 'blacklisted_words', 'print', 'builtins',
    'eval', 'blacklisted_chars', 'repr', 'main', 'subclasses', 'file',
    'class', 'mro', 'input', 'compile', 'init', 'doc', 'fork',
    'popen', 'read', 'map', 'dir', 'help', 'error', 'warning',
    'func_globals', 'vars', 'filter', 'debug', 'object', 'next',
    'word', 'base', 'prompt', 'breakpoint', 'class', 'pass',
    'chr', 'ord', 'iter', 'banned'
]
blacklisted_unicode = [
    '\u202e', '\u2060', '\u200f', '\u202a', '\u202b', '\u202c'
    '\u202d', '\u202f', '\u2061', '\u2062', '\u2063', '\u2064', '\ufeff'
]

blacklisted_chars = f'[{blacklisted_chars}]'
blacklisted_words = '|'.join(f'({word})' for word in blacklisted_words)
blacklisted_unicode_pattern = '|'.join(blacklisted_unicode)
blacklisted_nonascii = '[^\x00-\x7F]'

stdout = Nobuffers(sys.stdout)
stdout.write('''
                                                                         
        __..,,-----l"|-.                                                  
    __/"__  |----""  |  i--voo..,,__                                      
 .-'=|:|/\|-------o.,,,---. Y88888888o,,_                                 
_+=:_|_|__|_|   ___|__|___-|  """"````"""`----------.........___          
__============:' "" |==|__\===========(=>=+    |           ,_, .-"`--..._ 
  ;="|"|  |"| `.____|__|__/===========(=>=+----+===-|---------<---------_=-
 | ==|:|\/| |   | o|.-'__,-|   .'  _______|o  `----'|        __\ __,.-'"  
  "`--""`--"'"""`.-+------'" .'  _L___,,...-----------"""""""   "         
                  `------""""""""
       
''')

stdout.write('Enter command: ')
prompt = input()

prompt = prompt.encode('unicode-escape').decode('ascii')
prompt = bytes(prompt, 'ascii').decode('unicode-escape')

if re.findall(blacklisted_chars, prompt):
    raise Exception('Blacklisted character detected. Go away!')

if re.findall(blacklisted_words, prompt, re.I):
    raise Exception('Blacklisted word detected. Go away!')
    
if re.search(blacklisted_unicode_pattern, prompt):
    raise Exception('Blacklisted unicode detected. Go away!')
    
if re.search(blacklisted_nonascii, prompt):
    raise Exception('Non-ASCII character detected. Go away!')

try:
    exec(prompt)
except:
    pass

