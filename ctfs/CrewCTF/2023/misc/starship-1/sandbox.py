#!/usr/bin/env python3
import re
import sys

class Nobuffers:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines([f"{data}\n" for data in datas])
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

banned = re.escape('\\(~}?>{&/%`)<$|*=#!-+\'0123456789;[] ')
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

if prompt.isascii() and not re.findall(f'[{banned}]', prompt):
    try:
        exec(prompt, {'__builtins__': {'__build_class__': __build_class__, "__name__":__name__}})
    except:
        pass
