import hashlib, secrets, base64, sys

from pwnlib.tubes import remote

HOST = 'rps.sdc.tf'
PORT = 1337

def hash(m: bytes):
    return hashlib.md5(m).digest()

r = remote.remote(HOST, PORT)

def send(msg: str) -> None:
    r.sendline(msg.encode())

def send_data(msg: bytes) -> None:
    r.sendline(base64.b64encode(msg))

def recv() -> str:
    return r.recvline(keepends=False).decode()

def recv_command() -> 'tuple[str, str]':
    cmd, arg = recv().split(maxsplit=1)
    if cmd == '==': # skip proof-of-work if any
        cmd, arg = recv().split(maxsplit=1)
    return cmd, arg

def error(err: str):
    print(f'Server error: {err}')
    sys.exit(1)

def process_command():
    cmd, arg = recv_command()
    if cmd == 'ERROR':
        error(arg)
    elif cmd == 'MOVE':
        print(f'Server move: {arg}')
    elif cmd == 'VERDICT':
        print(f'Server verdict: {arg}')
        if arg == 'Client lost':
            print('Game over!')
            sys.exit(0)
    elif cmd == 'FLAG':
        print(f'You won the flag: {arg}')
        sys.exit(0)
    elif cmd == 'NEXT':
        print('Your turn!')
    else:
        error(f'Unknown command: {cmd}')

process_command()

while True:
    move = input('Input your move (R/P/S): ')
    pad = secrets.token_bytes(16)
    proof = move.encode() + pad
    commitment = hash(proof)
    send_data(commitment)
    process_command()
    send_data(proof)
    process_command()
    process_command()
