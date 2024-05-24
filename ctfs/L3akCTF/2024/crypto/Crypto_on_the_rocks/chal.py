from sage.all import *
from typing import Tuple
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import re
p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
K = GF(p)
a = K(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc)
b = K(0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00)
E = EllipticCurve(K, (a, b))
G = E(0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
E.set_order(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409 * 0x1)
n = G.order()


FLAG: str = open('flag.txt', 'r').read().strip()
KEY: int = randint(1, n - 1)
Q: int = KEY*G
AES_KEY = hashlib.sha256(long_to_bytes(KEY)).digest()

INVALID_ATTEMPTS = 0

def banner() -> str:
    banner = """\n
██████████╗░░█████╗░░█████╗░███████╗█
[=] ------------ Menu------------ [=]
[+] !1: Get Public Key            [+]
[+] !2: Sign a message            [+]
[+] !3: Verify a signature        [+]
[+] !4: Get the encrypted flag    [+]
[+] !5: Exit                      [+]
[=] ------------------------------[=]
██████████╗░░█████╗░░█████╗░███████╗█
\r\n"""
    return banner
def get_k() -> int:
    return int.from_bytes(hashlib.sha512(os.urandom(512//8)).digest(), byteorder='big') % n

def digest(msg) -> int:
    if isinstance(msg, str):
        msg = msg.encode()
    return int.from_bytes(hashlib.sha256(msg).digest(), byteorder='big')


def ecdsa_verify(Q, m, r, s) -> bool:
    e = digest(m)
    w = pow(s, -1, n)
    u1 = int((e * w) % n)  
    u2 = int((r * w) % n)  
    P = (u1 * G) + (u2 * Q)
    return r == int(P.xy()[0])


def ecdsa_sign(d: int, m: str) -> Tuple[int, int]:
    e = digest(m)
    k = get_k()
    P = k * G
    r_i = int(P.xy()[0])
    s_i = (pow(k, -1, n) * (e+r_i*d)) % n
    return (r_i, s_i)

def send_flag() -> str:
        flag = FLAG.encode()
        iv = get_random_bytes(16)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(flag, AES.block_size))
        return (iv + ct).hex()

def handle_signing() -> tuple:
    while True:
        try:
            inp = input("Enter message to sign. (`!exit`) to return to the main menu.\n\n>> ")
            if inp == "!exit":
                break
            r,s = ecdsa_sign(KEY, inp)
            print(f"Signature (r,s): {(r, s)}")
            
        except Exception as e:
            print(f"Error during signing: {e}")
            continue

def is_valid_format(inp) -> bool:
    pattern = r"^\([^,]+,\d+,\d+\)$"
    match = re.match(pattern, inp)
    return bool(match)

def handle_verfication():
    while True:
        inp = input("Enter the message you want to verify in the format `message,r,s` (`!exit` to return to the main menu).\n\n>> ")
        if inp == '!exit':
            break
        valid = is_valid_format(inp)
        if not valid:
            print("Invalid input format. Please try again.\n")
            continue
        message, r, s = inp.split(',')
        print(f"message: {message}\nr: {r}\ns: {s}\n")
        try:
            i_r, i_s = int(r), int(s)
            valid = ecdsa_verify(Q, message, i_r, i_s)
            result = "Signature is valid\n" if valid else "Signature is invalid\n"
            print(result)
        except Exception as e:
            print(f"Error during verification: {e}")
            continue
        


def process_option(option: str) -> str:
    global INVALID_ATTEMPTS
    if option == '!1':
        INVALID_ATTEMPTS = 0
        public_key_info = f"Public Key (X, Y): {Q.xy()}\n"
        print(public_key_info)
    elif option == '!2':
        INVALID_ATTEMPTS = 0
        handle_signing()
    elif option == '!3':
        INVALID_ATTEMPTS = 0
        handle_verfication()
    elif option == '!4':
        INVALID_ATTEMPTS = 0
        enc_flag = send_flag()
        print(f"Encrypted Flag: {enc_flag}\n")
    elif option == '!5':
        print("Goodbye!\n")
        return False
    else:
        INVALID_ATTEMPTS += 1
        print("Invalid option... Try again\n")
        if INVALID_ATTEMPTS >= 3:
            print("Too many invalid attempts. Exiting.\n")
            return False
    return True
        



def main():
    try:
        b = banner()
        print(b+"\n")
        while True:
            
            inp = input(">> ")
            if not process_option(inp):
                sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}, please try again later.\n")
        pass
    
    finally:
        sys.exit(0)

if __name__ == '__main__':
    main()
    
    