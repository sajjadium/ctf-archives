from Crypto.Util.number import getPrime
from os import urandom


def message(secret, e):
    m = f'The invite token is {secret.hex()} and it is encrypted with e = {e}.'.encode()
    return int.from_bytes(m, 'big')

def encrypt(data):
    out = []
    i = 0
    for pin in data:
        out.append((int(pin) + 5)^i)
        i+=1
    return out

def main():

    flag = open("flag.txt").read()

    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q

    secret = urandom(64)

    for _ in range(3):
        e = int(input("\nEnter your e: "))
        if e == 1: raise Exception('send me better values!')
        m = message(secret, e)
        c = encrypt(str(pow(m, e, n)))
        print(f'c = {c}')

    guess = input("Enter your invite code:")
    if secret != bytes.fromhex(guess): raise Exception('incorrect Invite code!')

    print(f'\nFLAG :{flag}')

if __name__ == '__main__':
    try:
        main()
    except:
        print('better luck next time!')
