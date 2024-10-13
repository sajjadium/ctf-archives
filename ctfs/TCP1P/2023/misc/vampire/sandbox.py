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

banned = re.escape('\\(~}?>{&/%`)<$|*=#!-+\'0123456789;@, ')
stdout = Nobuffers(sys.stdout)
stdout.write('''
        ,-.      _,---._ __  / \\
       /  )   .-'       `./ /   \\
      (  (   ,'            `/    /|
       \\  `-"             \\'   / |
        `.              ,  \\ \\ /  |
         /_`-.___    ___/`-._\\ `   |
        /_        `""`         _,\\'
       /_  .          o )   ,-`  )
      /_,-.`_._ _._  _,\\'`---`--"'
           `-._  /o )-`    
               `"\\""`
''')

stdout.write('Enter command: ')
prompt = input()

if prompt.isascii() and not re.findall(f'[{banned}]', prompt):
    try:
        eval(prompt, {'__builtins__': {'re': re}}, {})
    except:
        pass
