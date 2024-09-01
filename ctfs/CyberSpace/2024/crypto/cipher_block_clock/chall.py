import Crypto.Cipher.AES
import Crypto.Random
import Crypto.Util.Padding


f = b"CSCTF{placeholder}"
k = Crypto.Random.get_random_bytes(16)


def enc(pt):
    iv = Crypto.Random.get_random_bytes(32)
    ct = Crypto.Cipher.AES.new(iv, Crypto.Cipher.AES.MODE_CBC, k)
    return iv.hex(), ct.encrypt(Crypto.Util.Padding.pad(pt, 32)).hex()


iv0, ct0 = enc(f)
iv1, ct1 = enc(b"Lookie here, someone thinks that this message is unsafe, well I'm sorry to be the bearer of bad news but tough luck; the ciphertext is encrypted with MILITARY grade encryption. You're done kiddo.")


print(f"iv0: {iv0}\nct0: {ct0}\n")
print(f"iv1: {iv1}\nct1: {ct1}")