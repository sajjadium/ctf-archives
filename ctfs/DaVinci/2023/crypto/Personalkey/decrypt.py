from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import argparse
import hashlib

def decrypt_fct(private_key: int, iv: str, ciphertext: str) :
    derived_aes_key = hashlib.sha256(str(private_key).encode('ascii')).digest()
    cipher = AES.new(derived_aes_key, AES.MODE_CBC, bytes.fromhex(iv))
    return unpad(cipher.decrypt(bytes.fromhex(ciphertext)),16,'pkcs7').decode()
    # unpad can be remove if you don't have the dependencies

def main() :
    parser = argparse.ArgumentParser(description= "returns decrypted message, AES CBC Mode encryption")
    parser.add_argument("-k", "--key", type=str, help = "The secret key used must be given in its integer form", required=True)
    parser.add_argument("-iv", "--init_vector", type=str, help = "iv must be given in its hex value", required=True)
    parser.add_argument("-c", "--cipher", type=str, help = "cipher must be given in its hex value", required= True)
    args = parser.parse_args()
    try :
        key = int(args.key)
        iv = args.init_vector
        cipher = args.cipher
    except :
        raise Exception("Error in the inputs, please try -h for more infos")
    
    try:
        message = decrypt_fct(key, iv, cipher)
        print(message)
    except:
        print("Please, check your inputs because decryption isn't possible.")

if __name__ == '__main__':
    main()
