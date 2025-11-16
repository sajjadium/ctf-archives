#!/usr/bin/env python3

from sympy import randprime
from secrets import randbelow
from hashlib import sha512
from itertools import batched
from os import getenv
from sys import stdin
from tqdm import tqdm
import readline # python can't read more than 4095 bytes on a line without this!?!?!?!!?

bits = 1024
# P = randprime(1 << (bits - 1), 1 << bits)
P = 142183057539221114772334320155357900971672839527033419933632930422598689244699118628790550686385782087839264608691124166282411111453892566790501991185690337007365084640514843134915886806685595932682449190226519709045107875062749184557628698954376693978319256727395538290496585148574130635824813936971351780687
# G = randbelow(P)
G = 115773473808249193389699647223738486415484530297622716921274546881781790662447225064269223145484400140584983064539536225792083546317579179348492488582505669728734929584059156983199640635484135491292806628496468871748306724500896820885050766131662643822318998434410907162883100710397133922104461934169171994660

def get_flag(y: int, userid: int) -> None:
    print("Var god skriv in ett meddelande som säger att du får hämta flaggan\n> ", end="", flush=True)
    msg = stdin.buffer.readline()[:-1]
    print("Var god ange en passande skylttext till meddelandet\n> ", end="", flush=True)
    sgn = input()
    sgn = (
        int("".join(x), 16) for x in
        batched(sgn, bits // 4)
    )
    y1, *sgn = sgn
    if y != y1:
        return print("Vem har ens gjort den här?")

    h = sha512(msg)
    h.update(P.to_bytes(bits // 8) + G.to_bytes(bits // 8) + y.to_bytes(bits // 8))
    valid = True
    for c, ans in tqdm(batched(sgn, 2), total=128):
        h.update(c.to_bytes(bits // 8))
        if f"{int(h.hexdigest(), 16):b}".count("1") % 2:
            if pow(G, ans, P) != c:
                valid = False
                break
        else:
            if pow(G, ans, P) != c * y % P:
                valid = False
                break
        h.update(ans.to_bytes(bits // 8))
    if not valid:
        return print("Jättedålig skylttext >:(")

    if msg.decode("utf-8") == f"Kund nr. {userid} får hämta flaggan":
        print(getenv("FLAG") or "ingen flagga!?!?!?!?!?!?!?!?")
    else:
        print("Det verkar visst som att du inte får hämta någon flagga <:(")

def sign_message(y: int, x: int) -> None:
    print("Ange ett meddelande du vill ha en alldeles utmärkt skylttext till\n> ", end="", flush=True)
    msg = stdin.buffer.readline()[:-1]
    if b"flag" in msg:
        print("Ingen skylttext till det där inte >:(")
        return
    sgn = []
    h = sha512(msg)
    h.update(P.to_bytes(bits // 8) + G.to_bytes(bits // 8) + y.to_bytes(bits // 8))
    sgn.append(y)

    for _ in tqdm(range(128)):
        r = randbelow(P)
        c = pow(G, r, P)
        h.update(c.to_bytes(bits // 8))
        sgn.append(c)

        ans = r if f"{int(h.hexdigest(), 16):b}".count("1") % 2 else (x + r) % (P - 1)
        h.update(ans.to_bytes(bits // 8))
        sgn.append(ans)

    print("".join(f"{n:0{bits // 4}x}" for n in sgn))

def main():
    x = randbelow(P)
    y = pow(G, x, P)
    userid = randbelow(1000000)

    print(f"Välkommen, kund nr. {userid}!\n{P = }\n{G = }\n{y = }")
    while True:
        match input("Hämta [f]lagga eller [s]kylt? ")[0]:
            case "f":
                get_flag(y, userid)
            case "s":
                sign_message(y, x)

if __name__ == "__main__":
    raise SystemExit(main())
