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
it's the oracle again :)
ok ok, I promise to give you your poodle this time - not encrypted
just send me the word: givemetheflag
encrypted
with my secret key
that only I know
>:)
(add padding if needed of course... I know you can do it)
"""
tell_me = "\nWhat do you want to send me? ('nothing' to exit)\n>> "
def main():
    # load, encrypt and print the flag
    with open("flag.txt") as f:
        flag = f.read().strip().encode()
    with open("key.txt") as f:
        key = f.read().strip().encode()
    print(welcome_text)

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
            if b"givemetheflag" in dec_msg:
                print(f"nice work! {flag}")
            else:
                print("mmm... very interesting... thank you!")
        except ValueError:
            print("invalid padding >:(")
        except:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

if __name__ == "__main__":
    main()

