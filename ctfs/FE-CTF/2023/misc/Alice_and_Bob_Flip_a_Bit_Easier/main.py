#!/usr/bin/env python3
import json, os, random, mmap
from seccomp import SyscallFilter, Arg, ALLOW, EQ, MASKED_EQ, KILL

random = random.SystemRandom()
ROUNDS = 1000

def recv(io):
    fd, _ = io
    r = b''
    while True:
        c = os.read(fd, 1)
        if c in (b'', b'\0'):
            break
        r += c
    if not r:
        return
    return json.loads(r)

def send(io, data):
    _, fd = io
    os.write(fd, json.dumps(data).encode() + b'\0')

def close(io):
    i, o = io
    os.close(i)
    os.close(o)

def sandbox(code, name):
    pi, co = os.pipe()
    ci, po = os.pipe()
    pio = pi, po
    cio = ci, co
    pid = os.fork()
    if pid > 0:
        close(cio)
        def call(*args):
            send(pio, args)
            return recv(pio)
        return pid, call
    elif pid == 0:
        random.seed(0)

        flt = SyscallFilter(defaction=KILL)
        flt.add_rule(ALLOW, "write", Arg(0, EQ, co))
        flt.add_rule(ALLOW, "read",  Arg(0, EQ, ci))
        flt.add_rule(ALLOW, "mmap",  Arg(3, MASKED_EQ, mmap.MAP_ANONYMOUS, mmap.MAP_ANONYMOUS),
                                     Arg(4, EQ, 2**32-1),
                                     Arg(5, EQ, 0),
                     )
        flt.add_rule(ALLOW, "munmap")
        flt.add_rule(ALLOW, "brk")
        flt.load()

        exec(code)
        func = locals()[name]

        while True:
            args = recv(cio)
            if not args:
                break
            send(cio, func(*args))
        sys.exit(0)
    else:
        raise RuntimeError("Could not fork")

alice_pid, alice = sandbox(bytes.fromhex(input("alice> ")).decode(), "alice")
bob_pid, bob = sandbox(bytes.fromhex(input("bob> ")).decode(), "bob")

try:
    pairs = []
    for _ in range(ROUNDS):
        token = list(os.urandom(62))
        msg = alice(token)
        assert type(msg) == list and len(msg) <= 64 * 8 and all(x is True or x is False for x in msg)
        if msg: msg[random.randrange(0, len(msg))] ^= True
        pairs.append((token, msg))

    random.shuffle(pairs)

    for alice_token, msg in pairs:
        bob_token = bob(msg)
        assert alice_token == bob_token

    with open("flag", "r") as flag: print(flag.read())
finally:
    os.kill(alice_pid, 9)
    os.kill(bob_pid, 9)
