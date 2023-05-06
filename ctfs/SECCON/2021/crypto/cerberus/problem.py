import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from flag import flag
import signal

key = get_random_bytes(16)
block_size = 16

# encrypt by AES-PCBC
# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Propagating_cipher_block_chaining_(PCBC)
def encrypt(m):
    cipher = AES.new(key, AES.MODE_ECB)  # MODE_PCBC is not FOUND :sob: :sob:
    m = pad(m, 16)
    m = [m[i : i + block_size] for i in range(0, len(m), block_size)]

    iv = get_random_bytes(16)

    c = []
    prev = iv
    for m_block in m:
        c.append(cipher.encrypt(strxor(m_block, prev)))
        prev = strxor(c[-1], m_block)

    return iv, b"".join(c)


# decrypt by AES-PCBC
# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Propagating_cipher_block_chaining_(PCBC)
def decrypt(iv, c):
    cipher = AES.new(key, AES.MODE_ECB)  # MODE_PCBC is not FOUND :sob: :sob:
    c = [c[i : i + block_size] for i in range(0, len(c), block_size)]

    m = []
    prev = iv
    for c_block in c:
        m.append(strxor(prev, cipher.decrypt(c_block)))
        prev = strxor(m[-1], c_block)

    return b"".join(m)


# The flag is padded with 16 bytes prefix
# flag = padding (16 bytes) + "SECCON{..."
signal.alarm(3600)
ref_iv, ref_c = encrypt(flag)
print("I teach you a spell! repeat after me!")
print(base64.b64encode(ref_iv + ref_c).decode("utf-8"))

while True:
    c = base64.b64decode(input("spell:"))
    iv = c[:16]
    c = c[16:]

    if not c.startswith(ref_c):
        print("Grrrrrrr!!!!")
        continue

    m = decrypt(iv, c)

    try:
        unpad(m, block_size)
    except:
        print("little different :(")
        continue

    print("Great :)")
