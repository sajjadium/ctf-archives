from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

FLAG = open("flag.txt").read()


def load_public_key():
    with open('pub.pem', 'rb') as pubf:
        pubkey = serialization.load_pem_public_key(pubf.read(), backend=default_backend())
    return pubkey


def encrypt(pubkey:rsa.RSAPublicKey, ptxt:str) -> str:
    enc =  pubkey.encrypt(ptxt.encode(), padding.PKCS1v15())
    return b64encode(enc).decode()

def get_pem(key:rsa.RSAPrivateKey|rsa.RSAPublicKey):
    if isinstance(key, rsa.RSAPublicKey):
        pem = key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    else:
        pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    return pem


if __name__ == '__main__':

    pub_key = load_public_key()

    pub_key_pem = get_pem(pub_key).decode()

    enc_flag = encrypt(pub_key, FLAG)

    with open('flag.enc', 'w') as f:
        f.write(enc_flag)
