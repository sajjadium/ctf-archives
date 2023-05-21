import re

FLAG = open('flag.txt').read()

inp = input('> ')

if re.search(r'[123456789]', inp) or re.search(r'\(', inp) or eval(inp) != 1337:
    print('Nope')
else:
    print(FLAG)