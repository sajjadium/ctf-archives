from redacted import PRNG, FLAG
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    return iv+ciphertext

P = PRNG()
KEY = P.getBytes(16)
IV = P.getBytes(16)

print(f"Doofenshmirtz Evil Incorporated!!!\n")
print(f"All right, I don't like to repeat myself here but it just happens\nAnyhow, here's the encrypted message: {encrypt(KEY, FLAG, IV).hex()}\nOhh, How I love EVIL")
while True:
    iv = P.getBytes(16) 
    try:
        pt = input("\nPlaintext >> ")
        pt = bytes.fromhex(pt)
    except KeyboardInterrupt:
        break
    except:
        print("Invalid input")
        continue

    ct = encrypt(KEY, pt, iv)
    print(ct.hex())
