import os
from Derek import Derek

with open('flag.txt', 'rb') as f:
    flag = f.read()


banner = '''
██████╗ ███████╗██████╗ ███████╗██╗  ██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██║ ██╔╝
██║  ██║█████╗  ██████╔╝█████╗  █████╔╝ 
██║  ██║██╔══╝  ██╔══██╗██╔══╝  ██╔═██╗ 
██████╔╝███████╗██║  ██║███████╗██║  ██╗
╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                            
'''
print(banner)
key = os.urandom(16)
derek = Derek(key, rnd=42)
while True:
    print(
        '| Option:\n|\t[E]ncrypt\n|\t[D]ecrypt\n|\t[G]et encrypted flag\n|\t[Q]uit')
    option = input('> ')
    if option.lower() == 'e':
        print(derek.encrypt(bytes.fromhex(
            (input('msg you want to encrypt (in hex) > ')))).hex())
    elif option.lower() == 'd':
        print('unimplement')
    elif option.lower() == 'g':
        print(derek.encrypt(flag).hex())
    else:
        exit()
