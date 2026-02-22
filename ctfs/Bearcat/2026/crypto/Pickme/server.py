from Crypto.Util.number import bytes_to_long, isPrime, GCD
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

FLAG = bytes_to_long(open("flag.txt", "rb").read())


def get_multiline_input():
    lines = ""
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines += line + "\n"
        if line == "-----END RSA PRIVATE KEY-----":
            break
    return lines


def load_key():
    print("Enter your key in pem format:")
    pem = get_multiline_input().encode()
    try:
        key = load_pem_private_key(
            pem,
            password=None,
            backend=default_backend(),
            unsafe_skip_rsa_key_validation=True,
        )
    except:
        print("That doesn't look like a key to me...")
        return

    if isinstance(key, rsa.RSAPrivateKey):
        priv_numbers = key.private_numbers()
        pub_numbers = key.public_key().public_numbers()
    else:
        print("Hmm that's not right")
        return

    return priv_numbers, pub_numbers


def tests(priv, pub):
    phi = (priv.p - 1) * (priv.q - 1)
    if not isPrime(priv.p) or not isPrime(priv.q):
        return "I wouldn't call those primes"
    if priv.p.bit_length() < 512 or priv.q.bit_length() < 512:
        return "Primes are too small"
    if (priv.p - 1) * (priv.q - 1) != phi:
        return "That phi doesn't look quite right"
    if priv.p * priv.q != pub.n:
        return "That n doesn't look quite right"
    if pub.e < 65537:
        return "e is too small"
    if not isPrime(pub.e):
        return "e should be prime for best results"
    if pub.e.bit_count() > 2:
        return "This e is not efficient"
    if GCD(pub.e, phi) != 1:
        return "e must be coprime to phi"
    if (pub.e * priv.d) % phi != 1:
        return "d is invalid; it doesn't satisfy e * d ≡ 1 (mod phi)"
    if priv.dmp1 != (priv.d % (priv.p - 1)) or priv.dmq1 != (priv.d % (priv.q - 1)):
        return "Invalid CRT components"
    print("Key looks good, testing encryption capabilities...")
    m = FLAG
    c = pow(m, pub.e, pub.n)
    if m != pow(c, priv.d, pub.n):
        return f"Some unknown error occurred! Maybe you should take a look: {c}"


def main():
    print("Never worry about your RSA keys again!")
    print("Let me test them for you")
    print()

    key = load_key()
    if not key:
        return 1
    error = tests(*key)
    if error:
        print(f"An error occurred:\n{error}")
        return 1
    print("Looks good to me!")
    return 0


if __name__ == "__main__":
    main()
