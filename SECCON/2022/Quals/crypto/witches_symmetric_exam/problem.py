from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flag import flag, secret_spell

key = get_random_bytes(16)
nonce = get_random_bytes(16)


def encrypt():
    data = secret_spell
    gcm_cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    gcm_ciphertext, gcm_tag = gcm_cipher.encrypt_and_digest(data)

    ofb_input = pad(gcm_tag + gcm_cipher.nonce + gcm_ciphertext, 16)

    ofb_iv = get_random_bytes(16)
    ofb_cipher = AES.new(key, AES.MODE_OFB, iv=ofb_iv)
    ciphertext = ofb_cipher.encrypt(ofb_input)
    return ofb_iv + ciphertext


def decrypt(data):
    ofb_iv = data[:16]
    ofb_ciphertext = data[16:]
    ofb_cipher = AES.new(key, AES.MODE_OFB, iv=ofb_iv)

    try:
        m = ofb_cipher.decrypt(ofb_ciphertext)
        temp = unpad(m, 16)
    except:
        return b"ofb error"

    try:
        gcm_tag = temp[:16]
        gcm_nonce = temp[16:32]
        gcm_ciphertext = temp[32:]
        gcm_cipher = AES.new(key, AES.MODE_GCM, nonce=gcm_nonce)

        plaintext = gcm_cipher.decrypt_and_verify(gcm_ciphertext, gcm_tag)
    except:
        return b"gcm error"

    if b"give me key" == plaintext:
        your_spell = input("ok, please say secret spell:").encode()
        if your_spell == secret_spell:
            return flag
        else:
            return b"Try Harder"

    return b"ok"


print(f"ciphertext: {encrypt().hex()}")
while True:
    c = input("ciphertext: ")
    print(decrypt(bytes.fromhex(c)))
