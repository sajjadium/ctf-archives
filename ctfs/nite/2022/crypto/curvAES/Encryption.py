from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

curve = registry.get_curve('0x630x750x720x760x650x200x690x730x200x620x720x610x690x6e0x700x6f0x6f0x6c0x500x320x350x360x720x31')

def To256bit(point):
    algo = hashlib.sha256(int.to_bytes(point.x,32,'big'))
    algo.update(int.to_bytes(point.y,32,'big'))
    return algo.digest()

def encrypt_1(msg,secretKey):
    Cipher1 = AES.new(secretKey,AES.MODE_GCM)
    ciphertext,auth = Cipher1.encrypt_and_digest(msg)
    print(ciphertext , Cipher1.nonce , auth)
    return (ciphertext,Cipher1.nonce,auth)

def encrypt_2(msg,pubKey):
    ctPK = secrets.randbelow(curve.field.n)
    sharedKey = ctPK * pubKey
    secretKey = To256bit(sharedKey)
    ciphertext, nonce, auth = encrypt_1(msg, secretKey)
    ctPubK = ctPK * curve.g
    return (ciphertext, nonce, auth, PubKey)

privKey = 'Figure that out on your own :('
pubKey = privKey * curve.g

Encoded_message = encrypt_2(msg, pubKey)

encoded_message_details = {
    'ciphertext': binascii.hexlify(),
    'nonce': binascii.hexlify(),
    'auth': binascii.hexlify(),
    'PubKey': hex(??.x) + hex(??.y%2)[?:]
}