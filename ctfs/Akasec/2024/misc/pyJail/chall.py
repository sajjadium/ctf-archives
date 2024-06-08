import sys
from string import printable

print('''
#################################################################
#                                                               #
#   Welcome to pyJail!                                          #
#                                                               #
#   You have been jailed for using too many characters.         #
#                                                               #
#   You are only allowed to use 16 characters of printable      #
#   ascii.                                                      #
#                                                               #
#   If you manage to break free, you will get the flag.         #
#                                                               #
#################################################################\n''')

code = input('> ')

sys.stdin = None

len = sum(1 for char in code if char in printable)

if len >= 17:
    print('Too long!')
    exit()

eval(code)