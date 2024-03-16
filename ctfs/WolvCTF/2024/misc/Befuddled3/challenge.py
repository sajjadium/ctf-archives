from befunge import befunge, create_grid

import sys

code = input('code? ')
grid = create_grid(code + '\n')

if code == '':
    print('no code?')
    sys.exit(1)
if len(grid) > 1:
    print('must be a one liner!')
    sys.exit(1)
if len(grid[0]) > 8:
    print('too long :(')
    sys.exit(1)

befunge(grid, open('flag.txt').read())
