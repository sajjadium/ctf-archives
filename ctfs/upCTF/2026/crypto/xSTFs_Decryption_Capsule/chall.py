from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

KEY = os.urandom(16)

def print_banner():
    print("="*50)
    print("       Welcome to xSTF's decryption capsule!         ")
    print("="*50)
    print("Awaiting hex-encoded transmission...")

def main():
    print_banner()

    while True:
        try:
            line = input("\n>")
            if not line:
                break

            raw_data = line.strip()
            if raw_data.startswith("0x"): raw_data = raw_data[2:]

            data = bytes.fromhex(raw_data)
            if len(data) < 32:
                print("Incomplete Block")
                continue

            iv = data[:16]
            ciphertext = data[16:]

            cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)

            try:
                plaintext = unpad(decrypted, AES.block_size).decode('latin1')
            except Exception as e:
                print(str(e))
                continue


            if plaintext == "xSTF is the best portuguese CTF team :P":
                print("Yeah it is!")
                print(open("/flag.txt","r").read())
                return
            else:
                print(f"you ain't got lil bro")

        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    main()

