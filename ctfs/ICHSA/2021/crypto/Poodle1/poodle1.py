from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys, traceback

def encrypt(msg, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(msg, AES.block_size))

def decrypt(msg, key):
    iv = msg[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec_msg = cipher.decrypt(msg[AES.block_size:])
    return unpad(dec_msg, AES.block_size)

welcome_text = """hi there!
I am the oracle :D
searching for a poodle, huh?
what about that cute and encrypted poodle?

{}

BTW, if you want to tell me something don't forget to encrypt it
(with my secret key, of course ;))
"""
tell_me = "\nWhat do you want to tell me? ('nothing' to exit)\n>> "
def main():
    # load, encrypt and print the flag
    with open("flag.txt") as f:
        flag = f.read().strip().encode()
    with open("key.txt") as f:
        key = f.read().strip().encode()
    enc_flag = hexlify(encrypt(flag, key)).decode()
    print(welcome_text.format(enc_flag))

    while(True):
        try:
            # get input and respond
            msg = input(tell_me)
            if msg == "nothing":
                print("bye bye")
                break
            # decrpyt the given message
            enc_msg = unhexlify(msg)
            dec_msg = decrypt(enc_msg, key)
            print("mmm... very interesting... thank you!")
        except ValueError:
            print("invalid padding >:(")
        except:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

if __name__ == "__main__":
    main()
