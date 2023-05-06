from Crypto.Cipher import AES
import os

key = os.urandom(16)
iv = os.urandom(16)

modes = {
    'CBC': lambda:AES.new(key, AES.MODE_CBC, iv=iv),
    'CFB': lambda:AES.new(key, AES.MODE_CFB, iv=iv),
    'OFB': lambda:AES.new(key, AES.MODE_OFB, iv=iv),
    'CTR': lambda:AES.new(key, AES.MODE_CTR, nonce=b'', initial_value=iv),
    'EAX': lambda:AES.new(key, AES.MODE_EAX, nonce=iv),
    'GCM': lambda:AES.new(key, AES.MODE_GCM, nonce=iv),
}

print(r'''>>>>>> The Great TransMODEifier <<<<<<
*TRIAL VERSION*: Limited to three uses
                ______
             _.'______`._
           .'.-'      `-.`.
          /,' GCM    CBC `.\
         //          /     \\
========;;          /       ::========
        || EAX----()    CFB ||
========::                  ;;========
         \\                //
          \`. CTR    OFB ,'/
           `.`-.______.-'.'
             `-.______.-'

Usage: inputmode outputmode ciphertext''')

for i in ['1st','2nd','3rd']:
    try:
        inputmode, outputmode, ciphertext = input(f'{i} use: ').split()
        plaintext = modes[inputmode]().decrypt(bytes.fromhex(ciphertext))
        if plaintext == b'I Can Has Flag Plz?':
            from secret import flag
            plaintext = flag.encode()
        print(modes[outputmode]().encrypt(plaintext).hex())
    except Exception as e:
        print(repr(e))
print('Goodbye!')
