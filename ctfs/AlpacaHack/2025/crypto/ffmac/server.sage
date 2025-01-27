import os
import signal
from Crypto.Cipher import AES

signal.alarm(300)
FLAG = os.environ.get("FLAG", "Alpaca{*** FAKEFLAG ***}")

p = 2**127 - 1
k = 16
F = GF((p, k), "x")

def keygen():
    return [F.random_element() for _ in range(6)]


def to_list(el):
    return el.polynomial().padded_list(k)


def to_element(lst):
    return F(list(lst))


def ffmac(key, x):
    k1, k2, k3, k4, k5, k6 = key
    l, r = k1, x
    for i in range(127):
        if i % 2:
            r = r * l * k2
            l = l * l
        else:
            l = l * r * k3
            r = r * r
        l, r = r, l
    return k4 * l + k5 * r * x + k6


def encrypt(key, pt):
    cipher = AES.new(key, AES.MODE_CTR)
    return cipher.nonce + cipher.encrypt(pt)


mackey = keygen()
challenge = os.urandom(k)
print("Can you help to analyze the security of my new MAC scheme?")
while True:
    print("1. Compute MAC")
    print("2. Get flag")
    option = int(input("> "))
    if option == 1:
        inp = input("input: ").encode()
        if len(inp) != k or inp == challenge:
            print("invalid input")
            exit(1)
        mac_input = ffmac(mackey, to_element(inp))
        print(f"mac(input): {to_list(mac_input)}")
    elif option == 2:
        print(f"challenge: {challenge.hex()}")
        mac_list = [int(x) for x in input("mac: ").split(",")]
        if mac_list != to_list(ffmac(mackey, to_element(challenge))):
            print("invalid mac")
            exit(1)
        key = os.urandom(k)
        ciphertext = encrypt(key, FLAG.encode())
        print(f"ciphertext: {ciphertext.hex()}")
        mac_key = ffmac(mackey, to_element(key))
        print(f"mac(key): {to_list(mac_key)}")
        exit(0)
    else:
        print("invalid option")
        exit(1)
