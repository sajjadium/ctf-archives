
flag = input('Enter flag: ')

alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ0123456789{}_'
for x in flag:
    if not x in alph:
        print('Bad chars')
        exit(0)

import os
os.chdir('./RASP/')

import sys
sys.path.append('./RASP_support')

from REPL import REPL, LineReader

REPL.print_welcome = lambda *a, **kw: 0
r = REPL()

print('[*] Loading...')

r.run_given_line('set example "dice"')

with open('../berry.rasp', 'r') as f:
    r.run(fromfile=f, store_prints=False)

print('[*] Checking flag...')

lr = LineReader(given_line=f'res("{flag}");').get_input_tree()
rp = r.evaluate_tree(lr)
v = list(rp.res.val.get_vals())

if all(x == 1 for x in v):
    print('Correct :)')
else:
    print('Incorrect :(')
