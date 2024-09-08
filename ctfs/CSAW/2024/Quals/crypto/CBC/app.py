from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import os

def decrypt(txt: str) -> (str, int):
    try:
        token = bytes.fromhex(txt)

        c = AES.new(os.environ["AES_KEY"].encode(), AES.MODE_CBC, iv=os.environ["AES_IV"].encode())
        plaintext = c.decrypt(token)
        unpadded = unpad(plaintext, 16)
        
        return unpadded, 1
    except Exception as s:
        return str(s), 0

def main() -> None:
    while True:
        text = input("Please enter the ciphertext: ")
        text.strip()
        out, status = decrypt(text)
        if status == 1:
            print("Looks fine")
        else:
            print("Error...")

if __name__ == "__main__":
    main()


