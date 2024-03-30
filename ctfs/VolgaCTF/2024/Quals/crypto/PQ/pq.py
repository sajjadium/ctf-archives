from secret import flag
import gmpy2
import os


e = 65537


def generate_pq():
    seed_1 = os.urandom(256)
    seed_2 = os.urandom(128)

    p = gmpy2.next_prime(int.from_bytes(seed_1, 'big'))
    q = gmpy2.next_prime(p + int.from_bytes(seed_2, 'big'))

    return p, q


def crypt(text: bytes, number: int, n: int) -> bytes:
    encrypted_int = pow(int.from_bytes(text, 'big'), number, n)

    return int(encrypted_int).to_bytes(n.bit_length() // 8 + 1, 'big').lstrip(b'\x00')


def decrypt(ciphertext: bytes, d: int, n: int) -> bytes:
    decrypted_int = pow(int.from_bytes(ciphertext, 'big'), d, n)

    return int(decrypted_int).to_bytes(n.bit_length() // 8 + 1, 'big').lstrip(b'\x00')


if __name__ == '__main__':
    p, q = generate_pq()

    N = p * q

    print(N)
    print(crypt(flag, e, N))
