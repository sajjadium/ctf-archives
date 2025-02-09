#!/usr/bin/python3
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ecdsa import SigningKey, SECP256k1, VerifyingKey
import ecdsa
from secret import conversation_length,messages,secret

# Story setup
print("""
Alice and Bob are two secret agents communicating over a secure channel.
""")


alice_private_key = SigningKey.generate(curve=SECP256k1)
alice_public_key = alice_private_key.verifying_key

bob_private_key = SigningKey.generate(curve=SECP256k1)
bob_public_key = bob_private_key.verifying_key

def compute_shared_secret(private_key, public_key):
    shared_point = private_key.privkey.secret_multiplier * public_key.pubkey.point
    shared_secret_bytes = shared_point.to_bytes()
    return hashlib.sha256(shared_secret_bytes).digest()

shared_secret = compute_shared_secret(alice_private_key, bob_public_key)

aes_key = shared_secret[:16]
iv = shared_secret[16:]
random.seed(int(iv.hex(),16))

def encrypt(message):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext

def decrypt(ciphertext):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    try:
        plaintext = unpad(decrypted, AES.block_size)
        return plaintext
    except:
        return decrypted
def sign(message, private_key:SigningKey):
    message = message.encode()
    k = random.randint(1, SECP256k1.order - 1)  
    signature = private_key.sign(message,hashfunc=hashlib.sha256 ,k=k)
    return signature

def verify(message, signature, public_key:VerifyingKey):
    return public_key.verify(signature, message, hashfunc=hashlib.sha256)

def main():
    print(f"\nAlice's public key: {alice_public_key.to_string().hex()}")
    print(f"Bob's public key: {bob_public_key.to_string().hex()}")
    print("\nYour job is to break their scheme and get the secret key that is cuicial to their entire operation.")
    i = 0
    alice_flagged = False
    bob_flagged = False
    while i < conversation_length:
        message = messages[i]
        if i % 2 == 0:
            ciphertext = encrypt(message)
            signature = sign(message,alice_private_key)
            print(f"\nIntercepted from Alice:\nCiphertext: {ciphertext.hex()}\nSignature: {signature.hex()}\n")
            while True:
                try:
                    print(f"\nSend to Bob:")
                    ciphertext_forged = bytes.fromhex(input("Ciphertext (hex): "))
                    signature_forged = bytes.fromhex(input("Signature (hex): "))
                    
                    plaintext = decrypt(ciphertext_forged)
                    verified = verify(plaintext,signature_forged,alice_public_key)

                    break
                except ValueError as e:
                    if 'Data must be padded to 16 byte boundary in CBC mode' in str(e):
                        print("I thought you were an expert in this field. Don't you know that AES encrypted data needs to be in blocks of 16 bytes??!!")
                    elif 'non-hexadecimal number found in fromhex() arg' in str(e):
                        print("I thought you were better than this, you have actually dissapointed me, you need to input in hex.")
                    elif 'Padding is incorrect' in str(e):
                        print("Well Well Well, this operation is going to fail if you do not send the correct ciphertext.")
                    
                except ecdsa.keys.BadSignatureError:
                    if not alice_flagged:
                        print("\nI think they got suspicious, the signature did not match. Make sure the signature matches otherwise the whole operation is OVER!!")
                        print("Wait, I think I found something from their networks, they tried to decrypt the text and this is what they found:")
                        print(plaintext.hex())
                        alice_flagged = True
                    else:
                        print("AAAAGGHH!!! They got to us, I should not have trusted you in the first place. This operation is over. I REPEAT, THIS OPERATION IS OVER!!!!")
                        exit()
                    
        else:
            ciphertext = encrypt(message)
            signature = sign(message,bob_private_key)
            print(f"\nIntercepted from Bob:\nCiphertext: {ciphertext.hex()}\nSignature: {signature.hex()}\n")
            while True:
                try:
                    print(f"\nSend to Alice:")
                    ciphertext_forged = bytes.fromhex(input("Ciphertext (hex): "))
                    signature_forged = bytes.fromhex(input("Signature (hex): "))
                    
                    plaintext = decrypt(ciphertext_forged)
                    verified = verify(plaintext,signature_forged,bob_public_key)

                    break
                except ValueError as e:
                    if 'Data must be padded to 16 byte boundary in CBC mode' in str(e):
                        print("I thought you were an expert in this field. Don't you know that AES encrypted data needs to be in blocks of 16 bytes??!!")
                    elif 'non-hexadecimal number found in fromhex() arg' in str(e):
                        print("I thought you were better than this, you have actually dissapointed me, you need to input in hex.")
                    elif 'Padding is incorrect' in str(e):
                        print("Well Well Well, this operation is going to fail if you do not send the correct ciphertext.")
                    
                except ecdsa.keys.BadSignatureError:
                    print("\nI think they got suspicious, the signature did not match. Make sure the signature matches otherwise the whole operation is OVER!!")
                    if not bob_flagged:
                        print(plaintext.hex())
                        bob_flagged = True
                    else:
                        print("AAAAGGHH!!! They got to us, I should not have trusted you in the first place. This operation is over. I REPEAT, THIS OPERATION IS OVER!!!!")
                        exit()

        i += 1    
    print("\n")
    print("Great! Now they have no doubts that they are talking to each other. Now we will launch our attack. REMEMBER, WE ONLY GET ONE CHANCE!")
    print("Send this message to Alice:","Can I have the key again, I think I forgot where I kept the key.")
    try:
        print(f"\nSend to Aice:")
        ciphertext_forged = bytes.fromhex(input("Ciphertext (hex): "))
        signature_forged = bytes.fromhex(input("Signature (hex): "))
        
        plaintext = decrypt(ciphertext_forged)
        
        verified = verify(plaintext,signature_forged,bob_public_key)
        
        if verified and plaintext.decode() == "Can I have the key again, I think I forgot where I kept the key.":
            print("Very good, now we wait.")
            ciphertext = encrypt(secret)
            signature = sign(secret,alice_private_key)
            print(f"\nIntercepted from Alice:\nCiphertext: {ciphertext.hex()}\nSignature: {signature.hex()}\n")

    except ValueError as e:
        if 'Data must be padded to 16 byte boundary in CBC mode' in str(e):
            print("I thought you were an expert in this field. Don't you know that AES encrypted data needs to be in blocks of 16 bytes??!!")
        elif 'non-hexadecimal number found in fromhex() arg' in str(e):
            print("I thought you were better than this, you have actually dissapointed me, you need to input in hex.")
        elif 'Padding is incorrect' in str(e):
            print("Well Well Well, this operation is going to fail if you do not send the correct ciphertext.")
    except ecdsa.keys.BadSignatureError:
        print("AAAAGGHH!!! We were so close, I should not have trusted you in the first place. This operation is over. I REPEAT, THIS OPERATION IS OVER!!!!")
        exit()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
