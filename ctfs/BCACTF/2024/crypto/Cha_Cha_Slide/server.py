from Crypto.Cipher import ChaCha20

from os import urandom

key = urandom(32)
nonce = urandom(12)

secret_msg = urandom(16).hex()

def encrypt_msg(plaintext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(plaintext.encode()).hex()

print('Secret message:')
print(encrypt_msg(secret_msg))

print('\nEnter your message:')
user_msg = input()

if len(user_msg) > 256:
    print('\nToo long!')
    exit()

print('\nEncrypted:')
print(encrypt_msg(user_msg))

print('\nEnter decrypted secret message:')
decrypted_secret_msg = input()

if len(decrypted_secret_msg) == len(secret_msg):
    if decrypted_secret_msg == secret_msg:
        with open('../flag.txt') as file:
            print('\n' + file.read())
        exit()

print('\nIncorrect!')
