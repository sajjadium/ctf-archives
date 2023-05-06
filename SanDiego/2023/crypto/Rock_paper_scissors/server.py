import base64
import hashlib
import secrets
import sys
import traceback

flag = open('flag.txt').read()

N_ATTEMPTS = 100

def hash(m: bytes):
    return hashlib.md5(m).digest()

def command(cmd: str, arg: str):
    print(cmd, arg)

def error(msg: str):
    command('ERROR', msg)
    sys.exit(1)

num = {'R': 0, 'P': 1, 'S': 2}

LOSE = 'Client lost'

def get_verdict(cm: str, sm: str):
    nc = num[cm]
    ns = num[sm]
    if ns == (nc + 1) % 3:
        return LOSE
    elif ns == nc:
        return 'Draw'
    else:
        return 'Client won'

try:
    for i in range(N_ATTEMPTS):
        command('NEXT', '_')
        commit = base64.b64decode(input())
        server_move = secrets.choice('RPS')
        command('MOVE', server_move)
        proof = base64.b64decode(input())
        if len(proof) != 17:
            error('Incorrect proof length')
        if hash(proof) != commit:
            error('Client has bad commitment')
        client_move = chr(proof[0])
        if client_move not in 'RPS':
            error('Bad client move')
        ver = get_verdict(client_move, server_move)
        command('VERDICT', ver)
        if ver == LOSE:
            break
    else:
        command('FLAG', flag)
except Exception:
    traceback.print_exc()
    error('Exception')
