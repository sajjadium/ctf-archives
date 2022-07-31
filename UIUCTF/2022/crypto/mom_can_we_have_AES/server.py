from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

import random
import string

from fields import cert, block_size
from secret import flag

cipher_suite = {"AES.MODE_CBC" : AES.MODE_CBC, "AES.MODE_CTR" : AES.MODE_CTR, "AES.MODE_EAX" : AES.MODE_EAX, "AES.MODE_GCM" : AES.MODE_GCM,  "AES.MODE_ECB" : AES.MODE_ECB}

########## Client Hello ##########
# Enter encryption methods
input_encryptions_suite = input()
client_cipher_suite = input_encryptions_suite.split(", ")
# Enter client random
client_random = input()

########## Server Hello ##########

# Certificate
private_key = RSA.import_key(open("my_credit_card_number.pem").read())
cipher_hash = SHA256.new(cert)
signature = PKCS1_v1_5.new(private_key).sign(cipher_hash)
#Signed certificate
print(signature.hex())

# select cipher suite
selected_cipher_suite = {}
for method in cipher_suite:
    if method in client_cipher_suite:
        selected_cipher_suite[method] = cipher_suite[method]

if len(selected_cipher_suite) == 0:
    print("Honey, we have a problem. I'm sorry but I'm disowning you :(")
    exit()

# Selected cipher suite
print(*selected_cipher_suite.keys(), sep=', ')

server_random = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
# Server random
print(server_random)

########## ClientKeyExchange & CipherSpec Finished ##########
# Enter premaster secret
encrypted_premaster_secret = input()
cipher_rsa = PKCS1_OAEP.new(private_key)
premaster_secret = cipher_rsa.decrypt(bytearray.fromhex(encrypted_premaster_secret)).decode('utf-8')

session_key = SHA256.new((client_random + server_random + premaster_secret).encode()).hexdigest()
# Enter chosen cipher
chosen_cipher_name = input()
if chosen_cipher_name not in selected_cipher_suite:
    print("No honey, I told you we're not getting ", chosen_cipher_name, '.', sep='')
    exit()
cipher = AES.new(session_key.encode()[:16], cipher_suite[chosen_cipher_name])
# Enter encrypted finish
client_finish = input()
client_finish = bytearray.fromhex(client_finish)

########## ServerKeyExchange & CipherSpec Finished ##########

finish_msg = unpad(cipher.decrypt(client_finish), block_size)
assert(finish_msg == b'finish')

########## Communication ##########

# Listening...
while True:
    client_msg = input()
    client_msg = unpad(cipher.decrypt(bytearray.fromhex(client_msg)), block_size)

    if client_msg == flag:
        print("That is correct.")
    else:
        print("You are not my son.")
