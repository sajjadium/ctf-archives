#!/usr/bin/env python3
# crypto + misc challenge

# How to generate the authentication token
# Given as secret; key for AES, sign_key_pair for EdDSA ( sign_key, verify_key ), token, password
# key for AES, token, password were pre-shared to server.
# 1. Generate Signature for token over Ed25519 ( RFC8032 ) 
# 2. Encrypt password, token and signature with AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
# 3. Generate authentication token ; base64enc( iv for AES) || AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
# - password : 12 bytes, random bit-string
# - token : 15 bytes, random bit-string
# - signature : 64 bytes, Ed25519 signature ( RFC8032 )
# - key for AES : 32 bytes, random bit-string
# - iv for AES : 8 bytes, random bit-string
# - payload = base64enc(password || token || signature) : 124 bytes
# - authentication_token ( encrypted_payload ) = base64enc(iv) || AES-256-CTR-Enc ( payload ) : 136 bytes

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), './secret/'))
from client_secret import SIGN_KEY_PAIR_HEX
from common_secret import AES_KEY_HEX, TOKEN_HEX, PASSWORD_HEX

import base64
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Cipher import AES

AES_IV_HEX = "04ab09f1b64fbf70"
aes_iv = bytes.fromhex(AES_IV_HEX)

# load secrets
aes_key = bytes.fromhex(AES_KEY_HEX)
password = bytes.fromhex(PASSWORD_HEX)
token = bytes.fromhex(TOKEN_HEX)
sign_key_pair = ECC.import_key(bytes.fromhex(SIGN_KEY_PAIR_HEX).decode('ascii'))

# 1. Generate Signature for token over Ed25519 ( RFC8032 ) 
signer = eddsa.new(key=sign_key_pair, mode='rfc8032')
signature = signer.sign(token)

# 2. Encrypt password, token and signature with AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
payload = base64.b64encode(password+token+signature)
cipher = AES.new(key=aes_key, mode=AES.MODE_CTR, nonce=aes_iv)
# 3. Generate authentication token ; base64enc( iv for AES) || AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
encrypted_pwd_token_sig = cipher.encrypt(payload) 
encrypted_payload = base64.b64encode(aes_iv) + encrypted_pwd_token_sig

# user used PREVIOUS_AUTHN_TOKEN_HEX as authentication token
# print("PREVIOUS_AUTHN_TOKEN_HEX", encrypted_payload.hex())

print("PREVIOUS_ENCRYPTED_PWD_HEX", encrypted_pwd_token_sig[:16].hex())