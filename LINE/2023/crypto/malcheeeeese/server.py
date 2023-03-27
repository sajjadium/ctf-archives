#!/usr/bin/env python3

# crypto + misc challenge

# See generate_new_auth_token() in this file and client.py for details on the authentication token.

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), './secret/'))
from server_secret import FLAG
from common_secret import AES_KEY_HEX, TOKEN_HEX, PASSWORD_HEX

import base64
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

ENCRYPTED_PAYLOAD_SIZE = 136
PREVIOUS_ENCRYPTED_PWD = "72e124ff792af7bc2c077a0260ba3c4a"
AES_IV_HEX = "04ab09f1b64fbf70"
previous_aes_iv = bytes.fromhex(AES_IV_HEX)

# load secrets
aes_key = bytes.fromhex(AES_KEY_HEX)
previous_password = bytes.fromhex(PASSWORD_HEX)

# for authentication
previous_iv_b64 = base64.b64encode(previous_aes_iv)

replay_attack_filter_for_iv = [previous_iv_b64]
replay_attack_filter_for_sig = []
acceptable_token = [] # cf. previous token ( TOKEN_HEX ) was removed
acceptable_password = [b"cheeeeese"] # cf. previous password ( PASSWORD_HEX ) was removed


# Generate new token per request
# Output:
# - new authentication token
# - verifier for EdDSA
def generate_new_auth_token():
    # re-generate token+signature part
    # Generate authentication token ; base64enc( iv for AES ) || AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
    # Not changed : key for AES, iv for AES, password(PASSWORD_HEX)
    # Change : token, signature

    token = get_random_bytes(15)
    # 1. Generate Signature for token over Ed25519 ( RFC8032 ) 
    sign_key_pair = ECC.generate(curve='Ed25519')
    signer = eddsa.new(key=sign_key_pair, mode='rfc8032')
    signature = signer.sign(token)

    # 2. Encrypt password, token and signature with AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
    payload =  base64.b64encode(previous_password+token+signature)
    cipher = AES.new(key=aes_key, mode=AES.MODE_CTR, nonce=previous_aes_iv)
    # 3. Generate authentication token ; base64enc( iv for AES) || AES-256-CTR-Enc( base64enc(password || token || signature), key for AES, iv for AES )
    encrypted_payload = base64.b64encode(previous_aes_iv) + cipher.encrypt(payload) 
    
    # add token and signature to filter
    acceptable_token.append(token)
    replay_attack_filter_for_sig.append(base64.b64encode(token+signature)[20:])

    # prepare verifier for EdDSA
    verifier = eddsa.new(key=sign_key_pair.public_key(), mode='rfc8032')

    return encrypted_payload, verifier


# Input : b64password : base64 encoded password
# Output:
# - Is password verification successful? ( True / False )
# - raw passowrd length
# - Error Code ( 0, 1, 2 )
# - Error Message
def verify_password(b64password):
    try:
        password = base64.b64decode(b64password)
    except:
        return False, -1, 1, "Base64 decoding error"

    if password in acceptable_password:
        return True, len(password), 0, "Your password is correct!"
    return False, len(password), 2, "Your password is incorrect."

# Input : b64token_signature : base64 encoded token+signature, verifier, verify_counter
# Output:
# - Is signature verification successful? ( True / False )
# - Error Code ( 0, 1, 2, 3, 4 )
# - Error Message
def verify_signature(b64token_signature, verifier, verify_counter):
    b64token = b64token_signature[:20]
    b64signature = b64token_signature[20:]

    if verify_counter > 1:
        return False, 1, "Err1-Verification limit Error"

    if b64signature in replay_attack_filter_for_sig:
        return False, 2, "Err2-Deactived Token"
    
    try:
        token = base64.b64decode(b64token)
        signature = base64.b64decode(b64signature)
    except:
        return False, 3, "Err3-Base64 decoding error"
    
    try:
        verifier.verify(token, signature)
        if token in acceptable_token:
            return True, 0, "verification is successful"
    except ValueError:
        pass

    return False, 4, "Err4-verification is failed"

def decrypt(hex_ciphertext, verifier, verify_counter):

    flag = ""

    # Length check
    ciphertext = bytes.fromhex(hex_ciphertext)
    if len(ciphertext)!=ENCRYPTED_PAYLOAD_SIZE:
        ret = {
            "is_iv_verified" : False,
            "is_pwd_verified" : False,
            "pwd_len" : -1,
            "pwd_error_number" : -1,
            "pwd_error_reason": "",
            "is_sig_verified" : False,
            "sig_error_number" : -1,
            "sig_verification_reason": "authentication token size MUST be 136 bytes",
            "flag" : ""
        }
        return ret
    
    iv_b64 = ciphertext[:12]
    ciphertext = ciphertext[12:]

    # iv reuse detection
    if iv_b64 in replay_attack_filter_for_iv:
        ret = {
            "is_iv_verified" : False,
            "is_pwd_verified" : False,
            "pwd_len" : -1,
            "pwd_error_number" : -1,
            "pwd_error_reason": "",
            "is_sig_verified" : False,
            "sig_error_number" : -1,
            "sig_verification_reason": "iv reuse detected",
            "flag" : ""
        }
        return ret
    

    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=base64.b64decode(iv_b64))
    pt_b64 = cipher.decrypt(ciphertext)

    # password authentication
    is_pwd_verified, pwd_len, pwd_error_number, pwd_error_reason = verify_password(pt_b64[:16])

    # authentication using EdDSA
    is_sig_verified, sig_error_number, sig_error_reason = verify_signature(pt_b64[16:], verifier, verify_counter)

    if True==is_pwd_verified and True==is_sig_verified:
        flag = FLAG
    
    ret = {
        "is_iv_verified" : True,
        "is_pwd_verified" : is_pwd_verified,
        "pwd_len" : pwd_len,
        "pwd_error_number" : pwd_error_number,
        "pwd_error_reason": pwd_error_reason,
        "is_sig_verified" : is_sig_verified,
        "sig_error_number" : sig_error_number,
        "sig_error_reason": sig_error_reason,
        "flag" : flag
    }

    return ret
