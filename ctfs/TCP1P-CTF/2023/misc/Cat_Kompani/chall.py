#!/usr/bin/env python3

import string, sys

meow = '''|>Yy!G&vPBz:k-D;M+XxO?%ERqZ<VS`j#A/KC*L@$,WwFTNU^~I\\JQHh''' + string.whitespace + string.digits
hisss = ['import', 'builtins', 'sys', 'any', 'register', 'ord', 'ascii', 'string', 'exec', 'breakpoint', 'eval', 'compile', 'exit', 'print', 'meow', 'hisss', 'nyaa', 'miau', 'sh', 'code', 'bin', 'bash', 'dash', 'pop','write', 'open', 'read', 'pdb', 'run','dir', 'dict', 'file', 'main', 'name']
nyaa = input("What does the cat say? ")

if len(nyaa) > 200 or len(nyaa) < 100:
    print("\nGRrrr!!\n")
    sys.exit()

if any(miau for miau in nyaa if miau in meow):
    print('\nGRrrr!!\n')
    sys.exit()

if any(miau for miau in hisss if miau in nyaa):
    print('\nGRrrr!!\n')
    sys.exit()

if not nyaa.isascii():
    print('\nGRrrr!!\n')
    sys.exit()

try:
    eval(nyaa, {'__builtins__':None})
except:
    print("\nWe do not tolerate any human language here, THIS IS CAT COMPANY NYAAA!!\n")