import tenseal.sealapi as sealapi
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random, base64, os
FLAG = b"n1ctf{REDACTED}"
assert len(FLAG) == 48

degree = 4096
plain_modulus = sealapi.PlainModulus.Batching(degree, 18)
coeff = sealapi.CoeffModulus.BFVDefault(degree, sealapi.SEC_LEVEL_TYPE.TC128)
parms = sealapi.EncryptionParameters(sealapi.SCHEME_TYPE.BFV)
parms.set_poly_modulus_degree(degree)
parms.set_plain_modulus(plain_modulus)
parms.set_coeff_modulus(coeff)
ctx = sealapi.SEALContext(parms, True, sealapi.SEC_LEVEL_TYPE.TC128)

keygen = sealapi.KeyGenerator(ctx)
public_key = sealapi.PublicKey()
secret_key = keygen.secret_key()
keygen.create_public_key(public_key)

encryptor = sealapi.Encryptor(ctx, public_key)
decryptor = sealapi.Decryptor(ctx, secret_key)
encoder = sealapi.BatchEncoder(ctx)

def generate_poly():
    msg = [random.randint(0, 255) for _ in range(degree)]
    poly = f'{hex(msg[0])[2:]}'
    for i in range(1, len(msg)):
        if msg[i]: poly = f'{hex(msg[i])[2:]}x^{i} + {poly}'
    return sealapi.Plaintext(poly)

def print_enc(ct):
    ct.save("ct")
    print("[enc]", base64.b64encode(open("ct",'rb').read()).decode())

SLOTS = sorted(random.sample(range(0, degree), 16))
key = os.urandom(16)
M = [0 if i not in SLOTS else key[SLOTS.index(i)] for i in range(0, degree)]
plain, key_enc = sealapi.Plaintext(), sealapi.Ciphertext()

encoder.encode(M, plain)
encryptor.encrypt(plain, key_enc)
print_enc(key_enc)

for _ in range(32):
    opt = input("[?] ")
    if opt == "E":
        ct = sealapi.Ciphertext()
        encryptor.encrypt(generate_poly(), ct)
        print_enc(ct)
    elif opt == "D":
        open("dec", 'wb').write(base64.b64decode(input("[b64] ")))
        ct = sealapi.Ciphertext(ctx)
        ct.load(ctx, "dec")
        pt = sealapi.Plaintext()
        decryptor.decrypt(ct, pt)
        print("[*]", pt[0])
    else: break

print("[+]", AES.new(key, AES.MODE_CTR).encrypt(pad(FLAG, 16)).hex())