import hashlib
import random

methods = ['md5', 'sha256', 'sha3_256', 'sha3_512', 'sha3_384', 'sha1', 'sha384', 'sha3_224', 'sha512', 'sha224']

def random_encrypt(x) :
    method = random.choice(methods)
    hash_obj = hashlib.new(method)
    hash_obj.update(x.encode())
    return hash_obj.hexdigest()

def main() :
    message = open("tipsen_memory.txt", "r").read()
    enc = []

    for char in message :
        x = (ord(char) + 20) % 130
        x = hashlib.sha512(str(x).encode()).hexdigest()
        x = random_encrypt(x)
        enc.append(x)

    with open('encrypted_memory.txt', 'w') as f :
        f.write(str(enc))

if __name__ == "__main__" :
    main()