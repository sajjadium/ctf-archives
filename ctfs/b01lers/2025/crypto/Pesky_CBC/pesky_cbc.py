import secrets
from Crypto.Cipher import AES

try:
    with open('./flag.txt', 'r') as f:
        flag = f.read()
except:
    flag = 'bctf{REDACTED}'

key1 = secrets.token_bytes(32)
key2 = secrets.token_bytes(32)

def pesky_decrypt(ciphertext):
    assert len(ciphertext) % 16 == 0

    iv1 = secrets.token_bytes(16)
    iv2 = secrets.token_bytes(16)

    c1 = AES.new(key1, AES.MODE_CBC, iv1)
    c2 = AES.new(key2, AES.MODE_CBC, iv2)

    return c1.decrypt(c2.decrypt(ciphertext))

def main():
    cipher = AES.new(key2, AES.MODE_ECB)

    secret = secrets.token_bytes(16)
    ciphertext = cipher.encrypt(secret)

    print('Here is the encrypted secret:')
    print(ciphertext.hex())
    print()

    print('Here are some hints for you ^_^')
    for _ in range(8):
        random_value = secrets.token_bytes(16)
        ciphertext = cipher.encrypt(random_value)
        print(random_value.hex())
        print(ciphertext.hex())
    print()

    while True:
        print('Options:')
        print('1: pesky decrypt')
        print('2: guess secret')
        choice = input('>> ').strip()

        if choice == '1':
            ciphertext = bytes.fromhex(input('>> '))
            print(pesky_decrypt(ciphertext).hex())
        elif choice == '2':
            guess = bytes.fromhex(input('>> '))
            if secret == guess:
                print('Here is your flag :)')
                print(flag)
                return
            else:
                print('lmao skill issue')
                return
        else:
            print('Invalid Choice')
            return

if __name__ == '__main__':
    main()
    

