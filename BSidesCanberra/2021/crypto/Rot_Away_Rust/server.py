#!/usr/bin/python3

import json
import Crypto.Cipher.AES as aes
import Crypto.Random as rand
from binascii import *
import struct
import string
import sys

def debug_print(err):
    sys.stderr.write(err)

from RARsecrets import secrets_server

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

###################
## SERVER
###################

class RARServer:
    def __init__(self, secrets_server):
        self.secrets = secrets_server

    def step3r(self):
        ## Step 3 - receive
        step3r = input()
        try:
            step3rj = json.loads(step3r.strip())
        except Exception as e:
            err = "ERROR: Expecting JSON with keys session_id, ID_A, ID_B, gcm_cipher_AS, gcm_nonce_AS, gcm_tag_AS, gcm_cipher_BS, gcm_nonce_BS, gcm_tag_BS, failed: {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        ### Check all keys are included
        step3_keys = set(['session_id','ID_A', 'ID_B', 'gcm_cipher_AS', 'gcm_nonce_AS', 'gcm_tag_AS', 'gcm_cipher_BS', 'gcm_nonce_BS', 'gcm_tag_BS'])
        if step3_keys.issubset(set(step3rj.keys())) != True:
            err = "ERROR: Expecting JSON with keys session_id, ID_A, ID_B, gcm_cipher_AS, gcm_nonce_AS, gcm_tag_AS, gcm_cipher_BS, gcm_nonce_BS, gcm_tag_BS"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        ### Validate all entries
        if  (validate(step3rj['session_id'], "hex") != True) or \
            (validate(step3rj['ID_A'], "int", minimum=0, maximum=2**32) != True) or \
            (validate(step3rj['ID_B'], "int", minimum=0, maximum=2**32) != True) or \
            (validate(step3rj['gcm_cipher_AS'], "hex") != True) or \
            (validate(step3rj['gcm_nonce_AS'], "hex") != True) or \
            (validate(step3rj['gcm_tag_AS'], "hex") != True) or \
            (validate(step3rj['gcm_cipher_BS'], "hex") != True) or \
            (validate(step3rj['gcm_nonce_BS'], "hex") != True) or \
            (validate(step3rj['gcm_tag_BS'], "hex") != True):
            err = "ERROR: Found invalid hex string"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        ### Get appropriate key
        if not {step3rj['ID_A'], step3rj['ID_B']}.issubset( set(secrets_server.keys())):
            err = "ERROR: ID_A or ID_B not known "
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        K_AS = unhexlify(secrets_server[step3rj['ID_A']]['server_key'])
        K_BS = unhexlify(secrets_server[step3rj['ID_B']]['server_key'])

        ### Ensure session ID outside of cipher matches BOTH session_IDs inside cipher
        try:
            e3A = aes.new(K_AS, aes.MODE_GCM, nonce=unhexlify(step3rj['gcm_nonce_AS']))
            step3_plainA = e3A.decrypt_and_verify(unhexlify(step3rj['gcm_cipher_AS']), unhexlify(step3rj['gcm_tag_AS']))
        except Exception as e:
            err = "ERROR: GCM verify A failed {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        nonce_A_eA, session_id_eA, ID_A_eA, ID_B_eA = struct.unpack('4s8s2I', step3_plainA)

        try:
            e3B = aes.new(K_BS, aes.MODE_GCM, nonce=unhexlify(step3rj['gcm_nonce_BS']))
            step3_plainB = e3B.decrypt_and_verify(unhexlify(step3rj['gcm_cipher_BS']), unhexlify(step3rj['gcm_tag_BS']))
        except Exception as e:
            err = "ERROR: GCM verify B failed {}".format(e)
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        nonce_B_eB, session_id_eB, ID_A_eB, ID_B_eB = struct.unpack('4s8s2I', step3_plainB)

        ### Ensure session_id's provided match session_id's under both cipher
        if not (unhexlify(step3rj['session_id']) == session_id_eA == session_id_eB):
            err = "ERROR: Session ID provided does not match both encrypted session ids"
            print(json.dumps({"success":False, "error": err}))
            debug_print("external {}, eA {}, eB {}".format(step3rj['session_id'], hexlify(session_id_eA), hexlify(session_id_eB)))
            exit(-1)

        ### Ensure ID's provided match ID's under both cipher
        if not (step3rj['ID_A'] == ID_A_eA == ID_A_eB):
            err = "ERROR: ID_A provided does not match both encrypted ID_As"
            print(json.dumps({"success":False, "error": err}))
            debug_print("external {}, eA {}, eB {}".format(step3rj['ID_A'], ID_A_eA, ID_A_eB))
            exit(-1)

        if not (step3rj['ID_B'] == ID_B_eA == ID_B_eB):
            err = "ERROR: ID_B provided does not match both encrypted ID_Bs"
            print(json.dumps({"success":False, "error": err}))
            exit(-1)

        self.ID_A = ID_A_eA
        self.ID_B = ID_B_eA
        self.K_AS = K_AS
        self.K_BS = K_BS
        self.nonce_A = nonce_A_eA
        self.nonce_B = nonce_B_eB
        self.session_id = session_id_eA

        #print("DEBUG:\tnonce_A: {}\n\tsession_id: {}\n\tID_A: {}\n\tID_B: {}".format(hexlify(nonce_A_eA), hexlify(session_id_eA), hex(ID_A_eA), hex(ID_B_eA)))
        #print("DEBUG:\tnonce_A: {}\n\tsession_id: {}\n\tID_A: {}\n\tID_B: {}".format(hexlify(nonce_B_eB), hexlify(session_id_eB), hex(ID_B_eB), hex(ID_B_eB)))

    def step4s(self):
        ## Step 4 - Send
        ### Calculate random session key, send back, encrypted with both recipients server keys
        K_AB = rand.get_random_bytes(16)

        e4A = aes.new(self.K_AS, mode=aes.MODE_GCM)
        step4A_nonce = e4A.nonce
        (step4A_cipher, step4A_tag) = e4A.encrypt_and_digest(self.nonce_A + K_AB)

        e4B = aes.new(self.K_BS, mode=aes.MODE_GCM)
        step4B_nonce = e4B.nonce
        (step4B_cipher, step4B_tag) = e4B.encrypt_and_digest(self.nonce_B + K_AB)

        step4s = {  'success' : True,
                    'session_id' : hexlify(self.session_id).decode(),
                    'ID_A' : self.ID_A,
                    'ID_B' : self.ID_B,
                    'step4A_nonce' : hexlify(step4A_nonce).decode(),
                    'step4A_cipher' : hexlify(step4A_cipher).decode(),
                    'step4A_tag' : hexlify(step4A_tag).decode(),
                    'step4B_nonce' : hexlify(step4B_nonce).decode(),
                    'step4B_cipher' : hexlify(step4B_cipher).decode(),
                    'step4B_tag' : hexlify(step4B_tag).decode()
                }

        print(json.dumps(step4s))

    def print_directory(self):
        d = []
        for k in self.secrets.keys():
            if self.secrets[k]['name'] == 'guest':
                d.append( {'id': k, 'name' : self.secrets[k]['name'], 'affiliation' : self.secrets[k]['affiliation'], 'port' : 0, 'server_key' : self.secrets[k]['server_key'] } )
            else:
                d.append( {'id': k, 'name' : self.secrets[k]['name'], 'affiliation' : self.secrets[k]['affiliation'], 'port' : self.secrets[k]['port'] } )
        print(json.dumps(d))


    def show_menu(self):
        while(True):
            try:
                c = input("1) Show directory\n2) Key exchange\nq) Quit\nEnter Choice:")
            except Exception as e:
                print("ERROR in input. Closing... {}".format(e))
                exit(-1)

            if c.strip() == "1":
                self.print_directory()
                continue
            if c.strip() == "2":
                self.step3r()
                self.step4s()
                continue
            if c.strip() == 'q':
                exit(0)


###################
## MAIN
###################

if __name__ == "__main__":

    S = RARServer(secrets_server)
    S.show_menu()
