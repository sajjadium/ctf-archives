from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
import binascii
import os

KEY_SIZE = 16
NONCE_SIZE = 12
FLAG = "flag{lol_this_is_obv_not_the_flag}"

KEYS = []
CIPHERTEXTS = []
CIPHERTEXTS_LEN = 1

REQUEST = "gib me flag plis"

class Service:
    def __init__(self):
        self.key = self.gen_key()
        self.nonce = os.urandom(NONCE_SIZE)
        self.aad = b""

    def gen_key(self):
        self.key = os.urandom(KEY_SIZE)
        return self.key
    
    def decrypt(self, ciphertext, key):
        try:
            plaintext = AESGCMSIV(key).decrypt(self.nonce, ciphertext, self.aad)
            return plaintext
        except Exception:
            return None
        
usertext = ""

ASCII_BANNER = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                    CRYPTIC SERVICE                        ║
    ╚═══════════════════════════════════════════════════════════╝
    
            ∧_∧
           (･ω･)  Protecting your secrets one key at a time...
     
"""

print(ASCII_BANNER)
service = Service()
KEYS.append(service.key.hex())

MENU_HEADER = """
    ╔════════════════════════════════════╗
    ║          MAIN MENU                 ║
    ╚════════════════════════════════════╝
"""

while True:
    print(MENU_HEADER)
    print("Choose an option:")
    print("1. rotate key")
    print("2. debug")
    print("3. push ciphertext")
    print("4. request flag")

    choice = input("Your choice: ").strip()

    if choice == "1":
        service.gen_key()
        KEYS.append(service.key.hex())
        print("\nKey rotated.\n")

    elif choice == "2":
        print(f"\n{KEYS=}")
        print(f"{CIPHERTEXTS=}")
        print(f"nonce={service.nonce.hex()}\n")
    
    elif choice == "3":
        ct = input("\nEnter ciphertext (hex): ").strip()
        CIPHERTEXTS.append(ct)

        if len(CIPHERTEXTS) > CIPHERTEXTS_LEN:
            print("\nSorry, I cannot remember more ciphertexts :(\n")
            break
    
    elif choice == "4":
        for i in range(4):
            try:
                key = binascii.unhexlify(KEYS[i])
                ct = binascii.unhexlify(CIPHERTEXTS[i % len(CIPHERTEXTS)])

                text = service.decrypt(ct, key)[16 * i:16 * (i+1)].decode('utf-8').strip()
                if not text or len(text) == 0 or text is None:
                    print("why so rude :(\n")
                    exit(0)
            except Exception:
                print("you have no honour!\n")
                exit(0)

            usertext += text

        if usertext == REQUEST:
            print(f"Damn, you are something. Here is the flag: {FLAG}\n")
            exit(0)
        else:
            print("Request politely please!!\n")
            exit(0)
    else:
        print("I don't recognize this.")
