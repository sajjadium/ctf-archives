#!/usr/bin/env python3

import arrow
import json
import random
import sys

keys = {
    "a": 15498798452335698516189763255,
    "b": 4  
}

with open('flag') as f:
    flag = f.read()

with open('/dev/urandom', 'rb') as f:
    rand = f.read(8)

rand_int = int(rand.hex(), 16)

random.seed(rand_int)

offset = random.randint(-1623476442, 1623476442)


while True:
    sys.stdout.write('''Server's open..  for now
Would you like to get ->
  1. current time
  2. access to sanctum sanctorum
  3. goodbye
:''')
    sys.stdout.flush()
    response = input('')
    if response == '1':
        time = int(arrow.utcnow().timestamp()) - offset
        enc_time = pow(time, keys['b'], keys['a'])
        sys.stdout.write(
            'This NTP server has been taken over by time-travellers!!!\n')
        sys.stdout.write('Time mixed with sweet RSA!\n')
        sys.stdout.write(str(enc_time))
        sys.stdout.write('\n')
        sys.stdout.flush()
    elif response == '2':
        time = int(arrow.utcnow().timestamp()) - offset
        random.seed(time)
        guessing_int = random.randint(0, 99999999999)
        sys.stdout.write('''Only Dr.Strange with time-stone can access this area! To prove your worth guess the passcode by looking into the future!\n''')
        sys.stdout.flush()
        response = input('=> ')
        if response == str(guessing_int):
            sys.stdout.write('''Wow, guess you are a wizard, Harry XD\n''')
            sys.stdout.write(flag)
            sys.stdout.write('\n')
            break
        else:
            sys.stdout.write('''Imposter!''')
            sys.stdout.write('\n')
            break
    else:
        print('Farewell traveller...')
        break
