import hashlib
import random
import string
import itertools

LENGTH = 6
letter_set = string.ascii_letters + string.digits
hex_set = "0123456789abcdef"

def PoW_solve(given: str, h: str) -> str:
    for ch in itertools.product(hex_set, repeat=LENGTH):
        ch = ''.join(ch)
        if h == hashlib.md5(f"CHEF:{given}:{ch}".encode()).hexdigest():
            return ch

def PoW():
    a = ''.join(random.choice(letter_set) for i in range(20))
    b = ''.join(random.choice(hex_set) for i in range(LENGTH))
    h = hashlib.md5(f"CHEF:{a}:{b}".encode()).hexdigest()

    print("======== Proof-of-Work enabled ========")
    print(f"Send me a {LENGTH}-digit hex code (in lowercase) such that:")
    print(f"md5(\"CHEF:{a}:\" + \"<{LENGTH}-digit hex code>\") = {h}")
    
    ans = input("> ")
    if len(ans) != LENGTH:
        print("Length must be 6!")
        exit()

    if h != hashlib.md5(f"CHEF:{a}:{ans}".encode()).hexdigest():
        print("Proof-of-Work failed!")
        exit()

if __name__ == '__main__':
    PoW()
