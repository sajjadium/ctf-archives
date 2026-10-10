#!/usr/bin/python3

from redacted import FLAG

from Crypto.Util.number import bytes_to_long
from Crypto.Math.Numbers import Integer
from Crypto.PublicKey import RSA

import signal


TARGET = b'I challenge you to sign this message!'


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


def rsa(m, n, x):
    if not 0 <= m < n:
        raise ValueError("Value too large")
    return int(pow(Integer(m), x, n))


# Alice signs a message—"Hello Bob!"—by appending to the original 
# message a version encrypted with her private key. 
def wikipedia_sign(message, n, d):
    return rsa(message, n, d)


# Bob receives both the message and signature. He uses Alice's public key 
# to verify the authenticity of the message, i.e. that the encrypted copy,
# decrypted using the public key, exactly matches the original message.
def wikipedia_verify(message, signature, n, e):
    return rsa(signature, n, e) == bytes_to_long(message)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    rsa_key = RSA.generate(1024)
    public_key = (rsa_key.n, rsa_key.e)

    myprint(f"RSA public key: {public_key}")
    myprint("Options:")
    myprint(f"1 <sig> -- Submit signature for {TARGET} and win")
    myprint("2 <msg> -- Sign any other message using wikipedia-RSA")

    for _ in range(10):
        line = input("> ")
        action, data = map(int, line.split())
        if action == 1:
            if wikipedia_verify(TARGET, data, rsa_key.n, rsa_key.e):
                myprint(f"{FLAG}")
                exit(0)
            else:
                myprint(f"Nope. Keep trying!") 
        elif action == 2:
            if data % rsa_key.n == bytes_to_long(TARGET):
                myprint(f"Nope. Won't sign that!") 
            else:
                sig = wikipedia_sign(data, rsa_key.n, rsa_key.d)
            myprint(sig)
        else:
            break


if __name__ == "__main__":
    main()
