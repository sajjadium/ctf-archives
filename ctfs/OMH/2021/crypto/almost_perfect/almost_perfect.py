import random
import string

key_len = 14


def ensure_perfect_secrecy(data):
    assert all([len(c) <= key_len for c in data])


def encrypt(word, key):
    shifts = [ord(k) - ord('a') for k in key]
    pt = [ord(c) - ord('a') for c in word]
    return ''.join([chr(((p + shifts[i]) % len(string.ascii_lowercase)) + ord('a')) for i, p in enumerate(pt)])


def encrypt_data(data, key):
    ensure_perfect_secrecy(data)
    return " ".join([encrypt(word, key) for word in data])


def in_charset(c):
    return len(set(c).difference(set(string.ascii_lowercase))) == 0


def main():
    key = "".join([random.choice(string.ascii_lowercase) for _ in range(key_len)])
    print(key)
    data = open("data.txt", "rb").read().decode().split(" ")
    assert all([in_charset(c) for c in data])
    open('output.txt', 'wb').write(encrypt_data(data, key).encode())


main()
