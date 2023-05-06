import json
import os
from Crypto.Cipher import AES
import fluxtagram_leak1

############################################################################
pt = []
ct = []
ft = []
enc_flag = []
NUMBER_OF_PAIRS = 25
KEY = os.urandom(16)
FLAG = b'flag{secret_duh}'
############################################################################

def generate_plaintexts():
    global pt, NUMBER_OF_PAIRS

    print("[+] Generate Plaintexts", end='')
    for _ in range(NUMBER_OF_PAIRS):
        pt.append([int(i) for i in os.urandom(16)])
    print("\t\t\t ... done")

def generate_ciphertexts():
    global pt, ct, enc_flag, KEY

    print("[+] Generate Ciphertexts", end='')
    cipher = AES.new(KEY, AES.MODE_ECB)
    for i in range(len(pt)):
        ct.append([int (j) for j in cipher.encrypt(bytes(pt[i]))])
    print("\t\t ... done")
    
    print("[+] Encrypt Secret Ingredient", end='')
    enc_flag = [int (j) for j in cipher.encrypt(FLAG)]
    print("\t\t ... done")

    print("[+] Test Secret Ingredient Decryption", end='')
    if(cipher.decrypt(bytes(enc_flag)) == FLAG):
        print("\t ... done")
    else:
        print("\t ... ERROR")
        exit(0)

def generate_faulty_ciphertexts():
    global pt, ft, KEY

    print("[+] Test AES Implementation For Errors", end='')
    test = []
    for i in range(len(pt)):
        test.append(fluxtagram_leak1.encrypt_test(pt[i], [int(i) for i in KEY]))

    error = False
    for i in range(len(ct)):
        if(ct[i] != test[i]):
            error = True

    if(error):
        print("\t ... ERROR")
        exit(0)
    print("\t ... done")

    print("[+] Generate Faulty Ciphertexts", end='')
    for i in range(len(pt)):
        ft.append(fluxtagram_leak1.encrypt_faulty(pt[i], [int(i) for i in KEY]))
    print("\t\t ... done")

def challenge_output():
    global pt, ct, ft, enc_flag

    print("[+] Generate Challenge Output", end='')
    with open("plaintext.json", "w", encoding = 'utf-8') as f:
        f.write(json.dumps(pt))
    with open("ciphertext.json", "w", encoding = 'utf-8') as f:
        f.write(json.dumps(ct))
    with open("faulty_ciphertext.json", "w", encoding = 'utf-8') as f:
        f.write(json.dumps(ft))
    with open("secret_ingredient.json", "w", encoding = 'utf-8') as f:
        f.write(json.dumps(enc_flag))
    print("\t\t ... done")

def main():
    generate_plaintexts()
    generate_ciphertexts()
    generate_faulty_ciphertexts()
    challenge_output()
    print("[!] All Done! Happy Solving :)")

if __name__ == "__main__":
    main()