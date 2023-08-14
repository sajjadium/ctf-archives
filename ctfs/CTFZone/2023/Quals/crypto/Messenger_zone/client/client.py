import hmac
from pygost import gost34112012512
from pygost.gost3410 import sign, verify
from pygost.gost34112012 import GOST34112012
from pygost.gost3412 import GOST3412Kuznechik
from pygost.mgm import MGM
from pygost.mgm import nonce_prepare
from pygost import gost3410
from pygost.gost3413 import unpad2, pad2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from binascii import unhexlify
import time
import random
import requests

server_url = 'http://localhost:7777'
keys_api = '/keys'
get_api = '/get'
send_api = '/send'
register_api = '/register'
pubs_api = '/pubs'
getkeys_api = '/initkeys'

size = 64 
block_size = 16 
app_name = b'MessengerZone'
start_mes = b'MessengerZone_start'
MAX_SKIP = 10
nonce = nonce_prepare(b'\x00'*block_size)
start_time = int(time.time())
random.seed(start_time)

def long_to_bytes(val, endianness='big'):
    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    if endianness == 'little':
        s = s[::-1]
    return s

def point_to_bytes(point):
    return long_to_bytes(point[0]) + long_to_bytes(point[0])

def generate_bytes(n=size):
    return random.randbytes(n)

CURVE = gost3410.CURVES['id-tc26-gost-3410-2012-512-paramSetA']
        

def GENERATE_DH():
    prv_key = gost3410.prv_unmarshal(generate_bytes(64))
    pub_key = gost3410.public_key(CURVE, prv_key)
    return (prv_key, pub_key)

def DH(dh_pair, dh_pub):
    return CURVE.exp(dh_pair[0], *dh_pub)

def KDF_RK(rk, dh_out):
    data = point_to_bytes(dh_out)
    key = hmac.new(key=rk, msg=data, digestmod=GOST34112012).digest()
    return (key, key)

def KDF_CK(ck):
    key = hmac.new(key=ck, msg=b'\x00'*16, digestmod=GOST34112012).digest()
    return (key, key)

def ENCRYPT(mk, plaintext, associated_data):
    mgm = MGM(GOST3412Kuznechik(mk).encrypt, block_size)
    return mgm.seal(nonce, plaintext, associated_data)

def DECRYPT(mk, ciphertext, associated_data):
    mgm = MGM(GOST3412Kuznechik(mk).encrypt, block_size)
    return mgm.seal(nonce, ciphertext, associated_data)

def HEADER(dh_pair, pn, n):
    a = Header()
    a.dh = dh_pair[1]
    a.pn = pn
    a.n = n
    return a

def header_to_string(header):
    print([header.dh, header.pn, header.n])
    return ';'.join([str(header.dh[0]), str(header.dh[1]), str(header.pn), str(header.n)])

def string_to_header(string):
    l = string.split(';')
    dh_pub = (int(l[0]), int(l[1]))
    dh = [0, dh_pub]
    return HEADER(dh, int(l[2]), int(l[3]))

def CONCAT(ad, header):
    return ad + header_to_string(header).encode('utf-8')

class Header(object):
    pass

class Ratchet:
    def __init__(self, DHs, DHr, RK, CKs):
        self.DHs = DHs
        self.DHr = DHr
        self.RK = RK
        self.CKs = CKs
        self.CKr = None
        self.Ns = 0
        self.Nr = 0
        self.PN = 0
        self.MKSKIPPED = {}

    def RatchetEncrypt(self, plaintext, AD):
        self.CKs, mk = KDF_CK(self.CKs)
        header = HEADER(self.DHs, self.PN, self.Ns)
        self.Ns += 1
        return header, ENCRYPT(mk, plaintext, CONCAT(AD, header))
    
    def RatchetDecrypt(self, header, ciphertext, AD):
        plaintext = self._TrySkippedMessageKeys(header, ciphertext, AD)
        if plaintext != None:
            return plaintext
        if header.dh != self.DHr:                 
            self._SkipMessageKeys(header.pn)
            self._DHRatchet(header)
        self._SkipMessageKeys(header.n)             
        self.CKr, mk = KDF_CK(self.CKr)
        self.Nr += 1
        return DECRYPT(mk, ciphertext, CONCAT(AD, header))
    
    def _DHRatchet(self, header):
        self.PN = self.Ns                          
        self.Ns = 0
        self.Nr = 0
        self.DHr = header.dh
        self.RK, self.CKr = KDF_RK(self.RK, DH(self.DHs, self.DHr))
        self.DHs = GENERATE_DH()
        self.RK, self.CKs = KDF_RK(self.RK, DH(self.DHs, self.DHr))
    
    def _TrySkippedMessageKeys(self, header, ciphertext, AD):
        if (header.dh, header.n) in self.MKSKIPPED:
            mk = self.MKSKIPPED[header.dh, header.n]
            del self.MKSKIPPED[header.dh, header.n]
            return DECRYPT(mk, ciphertext, CONCAT(AD, header))
        else:
            return None

    def _SkipMessageKeys(self, until):
        if self.Nr + MAX_SKIP < until:
            raise Exception()
        if self.CKr != None:
            while self.Nr < until:
                self.CKr, mk = KDF_CK(self.CKr)
                self.MKSKIPPED[self.DHr, self.Nr] = mk
                self.Nr += 1



class Server:
    def __init__(self):
        self.open_vals = dict()
        self.messages = dict()
        self.first_messages = dict()
    
    def register(self, name, IK, PK, sig, OPK=[]):
        print('[*] User registration')
        print('name:',name)
        print('IK:',IK.hex())
        print('PK:',PK.hex())
        print('sig:',sig)
        data = {'name':name, 'IK':IK.hex(), 'PK': PK.hex(), 'sig':sig, 'OPK':str(OPK)}
        r = requests.post(server_url+register_api, json=data)
        return r.json()['message'] == 'User registration'
    
    def get_pubs(self, name):
        r = requests.get(server_url + pubs_api, params={'name':name})
        print(r.json())
        return r.json()
    
    def start_messages(self, m_from, IK_A, EK, m_to, mes):
        print('[*] Init chat')
        print('name:',m_from)
        print('IK:',IK_A)
        print('EK:',EK)
        print('To:',m_to)
        print('Msg:',mes)
        data = {'name':m_from, 'ik':IK_A, 'ek': EK, 'to':m_to, 'msg':mes.hex()}
        r = requests.post(server_url+keys_api, json=data)
        return r.json()['message'] == 'Init chat'


    def get_start_messages(self, m_to):
        print('[*] Get init chat msgs', m_to)
        r = requests.get(server_url + getkeys_api, params={'name':m_to})
        print(r.json())
        return r.json()['keys']

    
    def store_message(self, from_m, to_m, header, message):
        print('Save msg on server')
        print('To:',to_m)
        print('From:',from_m)
        print('header:',header)
        print('message:',message)

        data = {'from_m':from_m, 'to_m':to_m, 'header': header_to_string(header), 'message':message.hex()}
        print(data)
        r = requests.post(server_url+send_api, json=data)
        print(r.json())
        return r.json()['message'] == 'Save msg on server'
    
        
    def get_messages(self, to_m):
        print('Recive msgs', to_m)
        r = requests.get(server_url + get_api, params={'to_m':to_m})
        return r.json()['messages']

        

class Client:
    def __init__(self, name, server):
        self.name = name
        self.server = server
        self.IK_prv = gost3410.prv_unmarshal(generate_bytes(64))
        self.IK = gost3410.public_key(CURVE, self.IK_prv)
        print(name, 'IK', self.IK)
        self.PK_prv = gost3410.prv_unmarshal(generate_bytes(64))
        self.PK = gost3410.public_key(CURVE, self.PK_prv)
        print(name, 'PK', self.PK)
        self.RATCHET_dict = dict()
        
        dgst = gost34112012512.new(gost3410.pub_marshal(self.PK)).digest()[::-1]
        sig_PK = sign(CURVE, self.IK_prv, dgst)

        # register
        res = server.register(self.name, gost3410.pub_marshal(self.IK), gost3410.pub_marshal(self.PK), sig_PK.hex())
        print('Registered ',self.name,res)


    def start_x3dh(self, m_to):
        # x3dh as Alice
        keys = self.server.get_pubs(m_to)
        IK_B = gost3410.pub_unmarshal(bytes.fromhex(keys['IK']))
        print(m_to, 'IK', IK_B)
        PK_B = gost3410.pub_unmarshal(bytes.fromhex(keys['PK']))
        print(m_to, 'PK', PK_B)
        sig = bytes.fromhex(keys['sig'])
        OPK_B = keys['OPK']

        dgst = gost34112012512.new(gost3410.pub_marshal(PK_B)).digest()[::-1]
        if not verify(CURVE, IK_B, dgst, sig):
            print('Signature not valid')
            return False

        EK = gost3410.prv_unmarshal(generate_bytes(64))
        self.EK = EK
        EK_pub = gost3410.public_key(CURVE, EK)
        self.EK_pub = EK_pub

        DH1 = CURVE.exp(self.IK_prv, *PK_B)
        DH2 = CURVE.exp(EK, *IK_B)
        DH3 = CURVE.exp(EK, *PK_B)

        data_bytes = b'\x00'*32 + point_to_bytes(DH1) + point_to_bytes(DH2) + point_to_bytes(DH3)
        SK = HKDF(algorithm=hashes.SHA256(), length=size, salt=b'\x00'*size, info=app_name,).derive(data_bytes)
        print(self.name,'generated SK =', SK.hex())

        AD = gost3410.pub_marshal(self.IK) + gost3410.pub_marshal(IK_B)

        DHs_A=GENERATE_DH()
        RK_A, CKs_A = KDF_RK(SK, DH(DHs_A, PK_B))
        self.RATCHET_dict[m_to] = Ratchet(DHs=DHs_A, DHr=PK_B, RK=RK_A, CKs=CKs_A)

        mgm = MGM(GOST3412Kuznechik(SK).encrypt, block_size)
        ciphertext = mgm.seal(nonce, start_mes, AD)
        self.server.start_messages(self.name, self.IK, self.EK_pub, m_to, ciphertext)

        return True

    def receive_x3dh(self):
        for data in self.server.get_start_messages(self.name):
            # x3dh as bob
            m_from = data[0]
            IK_A = data[1]
            EK = data[2]
            m_to = data[3]
            mes = bytes.fromhex(data[4])
            if m_to != self.name:
                print('Message not for me')
            else:
                DH1 = CURVE.exp(self.PK_prv, *IK_A)
                DH2 = CURVE.exp(self.IK_prv, *EK)
                DH3 = CURVE.exp(self.PK_prv, *EK)

                data_bytes = b'\x00'*32 + point_to_bytes(DH1) + point_to_bytes(DH2) + point_to_bytes(DH3)
                SK = HKDF(algorithm=hashes.SHA256(), length=size, salt=b'\x00'*size, info=app_name,).derive(data_bytes)
                print(self.name,'generated SK =', SK.hex())

                AD = gost3410.pub_marshal(IK_A) + gost3410.pub_marshal(self.IK)
                mgm = MGM(GOST3412Kuznechik(SK).encrypt, block_size)
                dec_mes = mgm.open(nonce, mes, AD)
                if dec_mes != start_mes:
                    print('Start message invalid')
                else:
                    self.RATCHET_dict[m_from] = Ratchet(DHs=(self.PK_prv, self.PK), DHr=None, RK=SK, CKs=None)

    def send(self, m_to, msg, send=True):
        if m_to not in self.RATCHET_dict.keys():
                self.start_x3dh(m_to)

        msg = pad2(msg, block_size)
        AD = (self.name + m_to).encode('utf-8')
        head, cipher = self.RATCHET_dict[m_to].RatchetEncrypt(msg, AD)
        
        if send:
            print('SEND', header_to_string(head).encode('utf-8'), cipher, AD)
            self.server.store_message(self.name, m_to, head, cipher)
        return True

    def pull(self):
        msg_l = list()
        data_l = self.server.get_messages(self.name)
        for data in data_l:

            from_m = data['from_m']
            head = string_to_header(data['header'])
            cipher = bytes.fromhex(data['message'])
            AD = (from_m + self.name).encode('utf-8')
            print(from_m, data['header'], cipher, AD)
            if from_m not in self.RATCHET_dict.keys():
                self.receive_x3dh()
                
            print('PULL', header_to_string(head).encode('utf-8'), cipher, AD)
            msg = self.RATCHET_dict[from_m].RatchetDecrypt(head, cipher, AD)
            msg = unpad2(msg[:-2*block_size], block_size)
            msg_l.append((from_m, msg))

        return msg_l


def start_main():

    server = Server()
    client_dict = dict()
    current_client = 'A'
    print('Created client', current_client)
    client_dict[current_client] = Client(current_client, server)

    current_client = 'B'
    print('Created client', current_client)
    client_dict[current_client] = Client(current_client, server)

    while True:
        print('Client:',current_client)
        print('1 - Change client')
        print('2 - Send msg')
        print('3 - Pull msgs')
        print('q - quit')
        choose = input('> ')

        if choose == '1':
            if current_client == 'A':
                current_client = 'B'
            else:
                current_client = 'A'
            
            if current_client not in client_dict.keys():
                client_dict[current_client] = Client(current_client, server)
                print('Created client', current_client)

        elif choose == '2':
            if current_client == 'A':
                to_m = 'B'
            else:
                to_m = 'A'

            msg = input('Msg: ')
            r = client_dict[current_client].send(to_m, msg.encode('utf-8'))
            if r:
                print('Sended')
            else:
                print('Error')

        elif choose == '3':
            msgs = client_dict[current_client].pull()
            print('Msgs:')
            for msg in msgs:
                print(msg[0],':',msg[1].decode('utf-8'))


        elif choose == 'q':
            exit(0)
        else:
            print('Invalid choose')

start_main()