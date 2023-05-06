import json
import Crypto.Cipher.AES as aes
import Crypto.Random as rand
from binascii import *
import struct
import string
import argparse

from RARsecrets import flag
from RARsecrets import secrets_server as ss

def validate(value, check, minimum=None, maximum=None):
    valid_types = ["bool", "int", "hex"]

    if check not in valid_types:
        return False

    #Check for boolean
    if check == "bool":
        if type(value) == bool:
            return True
        else:
            return False

    #Check for valid int with optional min/max
    if check == "int":
        if type(value) != int:
            return False
        if (minimum == None) and (maximum == None):
            return True
        if (minimum == None) and (maximum != None):
            if value <= maximum:
                return True
            else:
                return False
        if (minimum != None) and (maximum == None):
            if value >= minimum:
                return True
            else:
                return False
        if (minimum != None) and (maximum != None):
            if (value >= minimum) and (value <= maximum):
                return True
            else:
                return False

    #Check for valid hex string
    if check == "hex":
        if type(value) != str:
            return False
        if all(c in string.hexdigits for c in value) == True:
            return True
        else:
            return False

#########################
#### RESPONDER
#########################

class ClientResponder:
    def __init__(self, client_id, client_server_key, friends_list, message):
        self.client_id = client_id
        self.K_BS = client_server_key
        self.friends_list = friends_list
        self.message = message

    def step1r(self):
        ## Step 1 - receive
        step1r = input()
        try:
            step1rj = json.loads(step1r.strip())
        except Exception as e:
            err = "ERROR: Expecting JSON with key ID_A, failed: {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        if 'ID_A' not in step1rj.keys():
            err = "ERROR: Expecting JSON with key ID_A, failed"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        ID_A = step1rj['ID_A']

        if validate(ID_A, "int", minimum=0, maximum=2**32) != True:
            err = "ERROR: ID_A not a valid integer"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        if ID_A not in self.friends_list:
            err = "ERROR: ID_A not in my friends list"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        self.step1rj = step1rj
        self.ID_A = ID_A

    def step2s(self):
        ## Step 2 - send
        nonce_b = rand.get_random_bytes(4)
        session_id = rand.get_random_bytes(8)
        id_a_packed = struct.pack("I", self.ID_A)
        id_b_packed = struct.pack("I", self.client_id)

        e2 = aes.new(self.K_BS, mode=aes.MODE_GCM)
        e2_gcm_nonce = e2.nonce

        (step2c, step2tag) = e2.encrypt_and_digest(nonce_b + session_id + id_a_packed + id_b_packed)

        step2s = {  'success' : True,
                    'session_id' : hexlify(session_id).decode(),
                    'ID_A' : self.ID_A,
                    'ID_B' : self.client_id,
                    'gcm_nonce' : hexlify(e2_gcm_nonce).decode(),
                    'gcm_cipher' : hexlify(step2c).decode(),
                    'gcm_tag' : hexlify(step2tag).decode()
                }

        print(json.dumps(step2s))

        self.step2s = step2s
        self.nonce_b = nonce_b
        self.session_id = session_id

    def step5r(self):
        ## Step 5 - receive
        step5r = input()

        try:
            step5rj = json.loads(step5r.strip())
        except Exception as e:
            err = "ERROR: Expecting JSON with key session_id, gcm_nonce, gcm_cipher, gcm_tag, failed: {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        step5_keys = set(['session_id', 'gcm_nonce', 'gcm_cipher', 'gcm_tag'])
        if step5_keys.issubset(set(step5rj.keys())) != True:
            err = "ERROR: Expecting JSON with key session_id, gcm_nonce, gcm_cipher, gcm_tag"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        ## Checks
        # 1. dec session_id is same as above
        # 2. nonce_b is same as above

        if  validate(step5rj['session_id'], "hex") != True or \
            validate(step5rj['gcm_nonce'], "hex") != True or \
            validate(step5rj['gcm_cipher'], "hex") != True or \
            validate(step5rj['gcm_tag'], "hex") != True  :

            err = "ERROR: Found invalid hex string"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        if unhexlify(step5rj['session_id']) != self.session_id:
            err = "ERROR: session_id mismatch"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        try:
            e5 = aes.new(self.K_BS, aes.MODE_GCM, nonce=unhexlify(step5rj['gcm_nonce']))
            step5_plain = e5.decrypt_and_verify(unhexlify(step5rj['gcm_cipher']), unhexlify(step5rj['gcm_tag']))
        except Exception as e:
            err = "ERROR: GCM verify failed {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        try:
            step5_dec_nonce, step5_dec_k_ab = struct.unpack('4s16s', step5_plain)
        except Exception as e:
            err = "ERROR: Incorrect decrypted format. Expecting (nonce_b || key) {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        if step5_dec_nonce != self.nonce_b:
            err = "ERROR: decrypted nonce_b mismatch"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        self.K_AB = step5_dec_k_ab

    def step6s(self):
        ### Step 6 - send
        e6 = aes.new(self.K_AB, mode=aes.MODE_GCM)
        e6_gcm_nonce = e6.nonce
        e6_gcm_cipher, e6_gcm_tag = e6.encrypt_and_digest(self.message)

        step6s = {  'success' : True,
                    'session_id' : hexlify(self.session_id).decode(),
                    'gcm_nonce' : hexlify(e6_gcm_nonce).decode(),
                    'gcm_cipher' : hexlify(e6_gcm_cipher).decode(),
                    'gcm_tag' : hexlify(e6_gcm_tag).decode()
                }

        print(json.dumps(step6s))

#########################
#### MAIN
#########################
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--clientid', type=int, default=9001, help="client_id of client_responder")
    args = parser.parse_args()

    client_id = args.clientid

    if client_id not in ss.keys():
        print("ERROR: Invalid client_id - {}".format(client_id))
        exit(-1)

    client_name = ss[client_id]['name']
    client_affiliation = ss[client_id]['affiliation'] #['cybears', 'decepticomtss', 'none']
    client_server_key = unhexlify(ss[client_id]['server_key'])

    if client_affiliation == 'none':
        friends_list = ss.keys()
    else:
        friends_list = []
        for k in ss.keys():
            if ss[k]['affiliation'] == client_affiliation:
                friends_list.append(k)

    if client_id == 9001: #Flagimus Prime
        message = flag
    else:
        message = b"Beep Bop Boop, handshake successful but I don't have the flag!"


    CR = ClientResponder(client_id, client_server_key, friends_list, message)
    CR.step1r()
    CR.step2s()
    CR.step5r()
    CR.step6s()
