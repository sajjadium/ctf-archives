from Crypto.Util.number import getPrime, long_to_bytes
from random import randint
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


with open("/flag", "rb") as f:
    flag = f.read().strip()

def main():
    print("[$] Did no one ever tell you to mind your own business??")

    g, p = 2, getPrime(1024)
    a = randint(2, p - 1)
    A = pow(g, a, p)
    print("[$] Public:")
    print(f"[$]     {g = }")
    print(f"[$]     {p = }")
    print(f"[$]     {A = }")

    try:
        k = int(input("[$] Choose k = "))
    except:
        print("[$] I said a number...")

    if k == 1 or k == p - 1 or k == (p - 1) // 2:
        print("[$] I'm not that dumb...")

    Ak = pow(A, k, p)
    b = randint(2, p - 1)
    B = pow(g, b, p)
    Bk = pow(B, k, p)
    S = pow(Bk, a, p)

    key = hashlib.md5(long_to_bytes(S)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    c = int.from_bytes(cipher.encrypt(pad(flag, 16)), "big")

    print("[$] Ciphertext using shared 'secret' ;)")
    print(f"[$]     {c = }")


if __name__ == "__main__":
    main()
