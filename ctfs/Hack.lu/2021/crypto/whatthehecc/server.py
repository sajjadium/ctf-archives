#!/usr/bin/env python3
import sys
import shlex
import subprocess
from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA3_256
from Cryptodome.Math.Numbers import Integer
import time 

# util

def run_cmd(cmd):
    try:
        args = shlex.split(cmd)
        return subprocess.check_output(args).decode('utf-8')
    except Exception as ex:
        return str(ex)


def read_message():
    return sys.stdin.readline()


def send_message(message):
    sys.stdout.write('### {0}\r\n>'.format(message))
    sys.stdout.flush()

# crypto stuff

def hash(msg):
    h_obj = SHA3_256.new()
    h_obj.update(msg.encode())
    return Integer.from_bytes(h_obj.digest())


def setup(curve):
    key = ECC.generate(curve=curve)
    return key


def blind(msg, pub):
    r = pub.pointQ * hash(msg)
    return r


def sign(r, key):
    r_prime = r * key.d.inverse(key._curve.order)

    date = int(time.time())
    nonce = Integer.random_range(min_inclusive=1,max_exclusive=key._curve.order)
    z = f'{nonce}||{date}'


    R = r_prime + (key._curve.G * hash(z))
    s = (key.d - hash(z)) % key._curve.order
    # return (R, s, z)
    # we can not give away z or this is unsafe: x = s+h(z)
    return R, s


def verify(msg, sig, pub):
    R, s = sig

    if s in [0,1,''] and s > 0:
        return False

    tmp1 = s * pub._curve.G
    tmp2 = - pub.pointQ 
    tmp3 = tmp2 + R

    return tmp1 + tmp3 == hash(msg) * pub._curve.G


## ok ok here we go

def main():
    while True:
        send_message('Enter your command:')
        cmd = read_message().strip()

        if cmd == 'sign':
            send_message('Send cmd to sign:')
            cmd = read_message().strip()

            if(cmd in ['id', 'uname', 'ls', 'date']):
                r = blind(cmd, pubkey)
                sig = sign(r, key)
                
                send_message(f'Here you go: {sig[0].x}|{sig[0].y}|{sig[1]}|{cmd}')
            else:
                send_message('Not allowed!')

        elif cmd == 'run':
            send_message('Send sig:')
            sig = read_message().strip()
            tmp = sig.split('|')
            if len(tmp) == 4:
                x = int(tmp[0])
                y = int(tmp[1])
                s = int(tmp[2])
                c = tmp[3]
                sig = (ECC.EccPoint(x, y, curve='P-256'), s)
                if(verify(c, sig, pubkey)):
                    out = run_cmd(c)
                    send_message(out)
                else:
                    send_message('Invalid sig!')
            else:
                send_message('Invalid amount of params!')

        elif cmd == 'show':
            send_message(pubkey)

        elif cmd == 'help':
            send_message('Commands: exit, help, show, run, sign')

        elif cmd == 'exit':
            send_message('Bye :) Have a nice day!')
            break

        else:
            send_message('Invalid command!')


if __name__ == '__main__':
    key = setup('P-256')
    pubkey = key.public_key()
    main()