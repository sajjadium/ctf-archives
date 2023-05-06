import json
import Crypto.Cipher.AES as aes
import Crypto.Random as rand
from binascii import *
import struct
from pwn import *
import argparse

class ClientInitiator:
    def __init__(self, responder_address, responder_port, server_address, server_port, client_id, client_server_key):
        self.client_id = client_id
        self.responder_address = responder_address
        self.responder_port = responder_port
        self.server_address = server_address
        self.server_port = server_port
        self.client_server_key = client_server_key

    def connect_to_responder(self):
        ####Initiator
        log.info("Connecting to Client Responder...")
        try:
            self.cr = remote(self.responder_address, self.responder_port)
        except Exception as e:
            log.error("ERROR: Could not connect to client responder: ({},{}) : {}".format(self.responder_address, self.responder_port, e))
            exit(-1)

    def step1s(self):
        ## Step 1 - send client_id to client_responder
        log.info("STEP 1 - send client_id to client_responder")
        self.cr.sendline(json.dumps({"ID_A" : self.client_id}))

    def step2r(self):
        ## Step 2 - receive from client_responder
        log.info("STEP 2 - receive from client_responder")
        step2r = self.cr.recvuntil(b'}')
        log.debug(step2r)

        try:
            step2rj = json.loads(step2r)
        except Exception as e:
            print("ERROR: Expecting JSON with key success, session_id, ID_A, ID_B, gcm_nonce, gcm_cipher, gcm_tag")
            exit(-1)

        step2r_keys = {'success', 'session_id', 'ID_A', 'ID_B', 'gcm_nonce', 'gcm_cipher', 'gcm_tag'}

        if 'success' in step2rj.keys():
            step2r_success = step2rj['success']
        else:
            print("ERROR: Expecting JSON with key success")
            exit(-1)

        if step2r_success != True:
            print("ERROR, step2r failed: {}".format(step2rj['error']))
            exit(-1)

        self.step2rj = step2rj

    def connect_to_server(self):
        log.info("STEP 3 - Send to server")
        try:
            self.s = remote(self.server_address, self.server_port)
        except Exception as e:
            log.error("ERROR: Could not connect to server: ({},{}) : {}".format(self.server_address, self.server_port, e))
            exit(-1)

    def get_directory(self):
        #requires active connection to server - run connect_to_server() first
        self.s.recvuntil(b'Choice:')
        self.s.sendline("1")
        d = self.s.recvuntil(b']')
        self.directory = json.loads(d)

    def step3s(self):
        ## Step 3 - send to server
        nonce_a = rand.get_random_bytes(4)
        log.debug("nonce_a : {}".format(hexlify(nonce_a)))
        id_a_packed = struct.pack("I", self.client_id)
        id_b_packed = struct.pack("I", self.step2rj['ID_B'])

        e3 = aes.new(self.client_server_key, mode=aes.MODE_GCM)
        gcm_nonce_AS = e3.nonce

        (gcm_cipher_AS, gcm_tag_AS) = e3.encrypt_and_digest(nonce_a + unhexlify(self.step2rj['session_id']) + id_a_packed + id_b_packed)

        step3s = {  'session_id' : self.step2rj['session_id'],
                    'ID_A' : self.client_id,
                    'ID_B' : self.step2rj['ID_B'],
                    'gcm_nonce_AS' : hexlify(gcm_nonce_AS).decode(),
                    'gcm_cipher_AS' : hexlify(gcm_cipher_AS).decode(),
                    'gcm_tag_AS' : hexlify(gcm_tag_AS).decode(),
                    'gcm_nonce_BS' : self.step2rj['gcm_nonce'], #Just pass on encrypted details from B to server
                    'gcm_cipher_BS' :  self.step2rj['gcm_cipher'],
                    'gcm_tag_BS':  self.step2rj['gcm_tag']
                }

        self.s.recvuntil(b'Choice:')
        self.s.sendline("2")
        self.s.sendline(json.dumps(step3s))
        self.step3s = step3s
        self.nonce_a = nonce_a

    def step4r(self):
        ## Step 4 - receive shared key from server
        log.info("STEP 4 - receive shared key from server")
        step4r = self.s.recvuntil(b'}')

        log.debug(step4r)

        try:
            step4rj = json.loads(step4r)
        except Exception as e:
            print("ERROR: Expecting JSON with key success, session_id, ID_A, ID_B, step4A_nonce, step4A_cipher, step4A_tag, step4B_nonce, step4B_cipher, step4B_tag")
            exit(-1)

        if 'success' in step4rj.keys():
            step4r_success = step4rj['success']
        else:
            print("ERROR: Expecting JSON with key success")
            exit(-1)

        if step4r_success != True:
            print("ERROR, step4r failed: {}".format(step4rj['error']))
            exit(-1)

        #Extract shared key
        e4 = aes.new(self.client_server_key, aes.MODE_GCM, nonce=unhexlify(step4rj['step4A_nonce']))
        try:
            step4_plain = e4.decrypt_and_verify(unhexlify(step4rj['step4A_cipher']), unhexlify(step4rj['step4A_tag']))
        except Exception as e:
            print("ERROR: GCM verify failed {}".format(e))
            exit(-1)

        step4_dec_nonce_a, step4_dec_k_ab = struct.unpack('4s16s', step4_plain)
        log.debug("nonce_a_e4 {}, K_AB {}".format(hexlify(step4_dec_nonce_a), hexlify(step4_dec_k_ab)))

        if step4_dec_nonce_a != self.nonce_a:
            print("ERROR: nonce_a mismatch under cipher")
            exit(-1)

        self.K_AB = step4_dec_k_ab
        self.step4rj = step4rj

    def step5s(self):
        ## Step 5 - send shared key to client_responder
        log.info("STEP 5 - send shared key to client_responder")

        step5s = {  'session_id' : self.step2rj['session_id'],
                    'gcm_nonce' : self.step4rj['step4B_nonce'], #Just pass on encrypted details from B to server
                    'gcm_cipher' :  self.step4rj['step4B_cipher'],
                    'gcm_tag':  self.step4rj['step4B_tag']
                }

        self.cr.sendline(json.dumps(step5s))

    def step6r(self):
        ## Step 6 - receive message from client_responder
        log.info("STEP 6 - receive message from client_responder ")
        step6r = self.cr.recvuntil(b'}')
        log.debug(step6r)

        step6rj = json.loads(step6r)

        try:
            e6 = aes.new(self.K_AB, mode=aes.MODE_GCM, nonce=unhexlify(step6rj['gcm_nonce']))
            log.success("MESSAGE RECEIVED! {}".format(e6.decrypt_and_verify(unhexlify(step6rj['gcm_cipher']), unhexlify(step6rj['gcm_tag']))))
        except Exception as e:
            print("ERROR in step 6 - decrypt message [{}]".format(e))
            exit(-1)

    def close_and_exit(self, status):
        #######################################################
        self.cr.close()
        self.s.close()
        exit(status)
        #######################################################


#############################################################
#### MAIN
#############################################################

if __name__ == "__main__":

    ## Extract command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--clientid', type=int, default=9006, help="client_id of client_initiator (default:guest)")
    parser.add_argument('-s', '--serveraddress',  default="localhost", help="server address (domain or IP string)")
    parser.add_argument('-t', '--responderaddress',  default="localhost", help="client responder address (domain or IP string)")
    parser.add_argument('-p', '--serverport', type=int, default=9000, help="Port number of server")
    parser.add_argument('-q', '--responderport', type=int, default=9007, help="Port number of client responder (default:echo)")
    parser.add_argument('-d', '--debug', help="Print debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        context.log_level = 'debug'
    else:
        context.log_level = 'info'

    server_address = args.serveraddress
    server_port = args.serverport
    responder_address = args.responderaddress
    responder_port = args.responderport

    log.debug("s_add - {}\ns_port - {}\ncr_add - {}\ncr_port - {}".format(server_address, server_port, responder_address, responder_port))

    client_id = args.clientid

    ## Get server directory - find guest and echo users
    log.info("Connecting to server to download directory")
    try:
        server = remote(server_address, server_port)
    except Exception as e:
        log.error("ERROR: Could not connect to server: ({},{}) : {}".format(server_address, server_port, e))
        exit(-1)

    server.recvuntil(b'Choice:')
    server.sendline("1")
    d = server.recvuntil(b']')
    dj = json.loads(d)

    friends_list = []

    for user in dj:
        if user['name'] == 'guest': #get our server key
            client_server_key = unhexlify(user['server_key'])
            client_name = user['name']
            client_id = user['id']
            client_affiliation = user['affiliation']
        if user['name'] == 'echo': #get echo's port
            responder_port = user['port']
        if user['affiliation'] == 'none':
            friends_list.append(user['id'])


    log.debug("DEBUG: \n\tclient_id - {}\n\tclient_name - {}\n\tclient_affiliation - {}\n\tfriends_list - {}".format(client_id, client_name, client_affiliation, friends_list))

    ## Start Client Initiator Protocol run
    CI = ClientInitiator(responder_address, responder_port, server_address, server_port, client_id, client_server_key)
    CI.connect_to_responder()
    CI.step1s()
    CI.step2r()
    CI.connect_to_server()
    CI.get_directory()
    log.info(str(CI.directory))
    CI.step3s()
    CI.step4r()
    CI.step5s()
    CI.step6r()
    CI.close_and_exit(0)
