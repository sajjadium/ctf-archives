from Crypto.Util.number import long_to_bytes,bytes_to_long,getPrime,inverse
from gmssl.SM4 import CryptSM4,SM4_ENCRYPT,xor
from hashlib import sha256
from secret import secret
import signal
import time
import json
import os

FLAG = b'ant' + secret

banner = br"""
 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
'########::::'###::::'#######::::::'######::'########:'########:::::'#######::::'#####::::'#######:::'#######::
 ##.... ##::'## ##::'##.... ##::::'##... ##:... ##..:: ##.....:::::'##.... ##::'##.. ##::'##.... ##:'##.... ##:
 ##:::: ##:'##:. ##:..::::: ##:::: ##:::..::::: ##:::: ##::::::::::..::::: ##:'##:::: ##:..::::: ##:..::::: ##:
 ##:::: ##:..:::..:::'#######::::: ##:::::::::: ##:::: ######:::::::'#######:: ##:::: ##::'#######:::'#######::
 ##:::: ##:::::::::::...... ##:::: ##:::::::::: ##:::: ##...:::::::'##:::::::: ##:::: ##:'##:::::::::...... ##:
 ##:::: ##::::::::::'##:::: ##:::: ##::: ##:::: ##:::: ##:::::::::: ##::::::::. ##:: ##:: ##::::::::'##:::: ##:
 ########:::::::::::. #######:::::. ######::::: ##:::: ##:::::::::: #########::. #####::: #########:. #######::
 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

MENU1 = br'''
 ====------------------------------------------------------------------------------------------------------====
 |    |              +---------------------------------------------------------------------+              |   |
 |    |              |            [R]egister     [L]ogin     [T]ime     [E]xit             |              |   |
 |    |              +---------------------------------------------------------------------+              |   |
 ====------------------------------------------------------------------------------------------------------====
'''

MENU2 = br'''
 ====------------------------------------------------------------------------------------------------------====
 |    |              +---------------------------------------------------------------------+              |   |
 |    |              |            [G]et_dp_dq     [F]lag     [T]ime     [E]xit             |              |   |
 |    |              +---------------------------------------------------------------------+              |   |
 ====------------------------------------------------------------------------------------------------------====
'''

def pad(msg):
    tmp = 16 - len(msg)%16
    return msg + bytes([tmp] * tmp)

def get_token(id:str,nonce:str,_time:int):
    msg = {"id":id,"admin":0,"nonce":nonce,"time":_time}
    return str(json.dumps(msg)).encode()

class CRT_RSA_SYSTEM:
    nbit = 1024
    blind_bit = 128
    unknownbit = 193

    def __init__(self):
        e = 0x10001
        p,q = [getPrime(self.nbit // 2) for _ in "AntCTF"[:2]]
        n = p * q
        self.pub = (n,e)

        dp = inverse(e,p - 1)
        dq = inverse(e,q - 1)
        self.priv = (p,q,dp,dq,e,n)
        self.blind()

    def blind(self):
        p,q,dp,dq,e,n = self.priv
        rp,rq = [getPrime(self.blind_bit) for _ in "D^3CTF"[:2]]
        dp_ = (p-1) * rp + dp
        dq_ = (q-1) * rq + dq
        self.priv = (p,q,dp_,dq_,e,n)

    def get_priv_exp(self):
        p,q,dp,dq,e,n = self.priv
        dp_ = dp & (2**(self.nbit//2 + self.blind_bit - self.unknownbit) - 1)
        dq_ = dq & (2**(self.nbit//2 + self.blind_bit - self.unknownbit) - 1)
        return (dp_,dq_)

    def encrypt(self,m):
        n,e = self.pub
        return pow(m,e,n)

    def decrypt(self,c):
        p,q,dp,dq,e,n = self.priv
        mp = pow(c,dp,p)
        mq = pow(c,dq,q)
        m = crt([mp,mq],[p,q])
        assert pow(m,e,n) == c
        return m

class SM4_CTR(CryptSM4):
    block_size = 16

    def _get_timers(self, iv, msgLen):
        blockSZ = self.block_size
        blocks = int((msgLen + blockSZ - 1) // blockSZ)
        timer = bytes_to_long(iv)
        timers = iv
        for i in range(1, blocks):
            timer += 1
            timers += long_to_bytes(timer)
        return timers

    def encrypt_ctr(self, input_data,count = None):
        assert len(input_data) % self.block_size == 0
        if count == None:
            count = os.urandom(16)

        counters = self._get_timers(count,len(input_data))
        blocks = xor(self.crypt_ecb(counters), input_data)
        ciphertext = bytes(blocks)
        return count + ciphertext[:len(input_data)]

    def decrypt_ctr(self, input_data):
        assert len(input_data) % self.block_size == 0
        pt = self.encrypt_ctr(input_data[self.block_size:], input_data[:self.block_size])
        return pt[self.block_size:]

class D3_ENC:
    def __init__(self,key:bytes,authdate:bytes):
        self.crt_rsa = CRT_RSA_SYSTEM()
        self.block = SM4_CTR()

        self.block.set_key(key, SM4_ENCRYPT)
        self.authdate = bytes_to_long(authdate)

    def encrypt(self,msg):
        assert len(msg) % 16 == 0

        cipher = self.block.encrypt_ctr(msg)
        tag = self.get_tag(msg)
        return cipher,tag

    def decrypt(self,cipher):
        assert len(cipher) % 16 == 0

        msg = self.block.decrypt_ctr(cipher)
        tag = self.get_tag(msg)
        return msg,tag

    def get_tag(self,msg):
        auth_date = self.authdate
        msg_block = [bytes_to_long(msg[i*16:(i+1)*16]) for i in range(len(msg)//16)]

        for mi in msg_block:
            auth_date = int(sha256(str(self.crt_rsa.encrypt(auth_date)).encode()).hexdigest()[:32],16) ^ mi

        return int(sha256(str(self.crt_rsa.encrypt(auth_date)).encode()).hexdigest()[:32],16)

class D3_SYS:
    def register(self):
        print('Welcome to D^3 CTF 2023!')

        username = input("[D^3] USERNAME:")
        if username in self.UsernameDict:
            print(f'[D^3] Sorry,the USERNAME {username} has been registered.')
            return 

        elif len(username) >= 20:
            print('[D^3] Sorry,the USERNAME can\'t be longer than 20.')
            return

        nonce = os.urandom(8).hex()

        token = get_token(username,nonce,int(time.time()))
        cipher_token,tag = self.d3block.encrypt(pad(token))
        self.UsernameDict[username] = tag
        print('[D^3] ' + username + ', token is ' + cipher_token.hex() + '& nonce is ' + nonce)

    def login(self):
        print('Welcome to D^3 CTF 2023!')

        username = input("[D^3] USERNAME:")

        if username not in self.UsernameDict:
            print('[D^3] Sorry,the username has never been registered.')
            return False

        veritag = self.UsernameDict[username]
        cipher_token = bytes.fromhex(input("[D^3] Token:"))
        try:
            msg,tag = self.d3block.decrypt(cipher_token)
        except:
            print("[D^3] Something Wrong...quiting....")
            return False

        if tag != veritag :
            print('[D^3] Ouch! HACKER? Get Out!')
            return False

        try:
            token_dict = json.loads(msg.decode('latin-1').strip().encode('utf-8'))
        except:
            print('[D^3] Sorry,try again plz..')
            return False

        ID = token_dict["id"]
        if ID != username:
            print('[D^3] Change name?')
            return False

        elif abs(int(time.time()) - token_dict['time']) >= 1:
            print('[D^3] oh...no...out....')
            return False

        elif token_dict['admin'] != True:
            print("[D^3] Logining.")
            return False

        else:
            print("[D^3] Logining.")
            return True

    def time(self):
        print('[D^3] D^3\' clock shows '+str(int(time.time())))
        return

    def get_dp_dq(self):
        return self.d3block.crt_rsa.get_priv_exp()

    def enc_flag(self):
        flag = FLAG + os.urandom(16)
        n,e = self.d3block.crt_rsa.pub
        enc_flag = pow(bytes_to_long(flag),e,n)
        return enc_flag

    def handle(self):
        print(banner.decode())

        key = os.urandom(16)
        authdate = os.urandom(16)
        self.d3block = D3_ENC(key,authdate)
        print('[D^3] My initial Authdate is ' + authdate.hex())
        print('[D^3] My Auth pubkey is ' + str(self.d3block.crt_rsa.pub))
        self.UsernameDict = {}

        admin = None
        # signal.alarm(60) # in server.......
        while 1:
            print(MENU1.decode())
            option = input('option >')
            if option == 'R':
                self.register()
            elif option == 'L':
                admin = self.login()
                break
            elif option == 'T':
                self.time()
            else:
                break

        if admin != True:
            print("ByeBye! You are not admin.......")
            exit()

        print("Hello,Admin.Now, you have 2 chances to operate.")
        for __ in 'D^3 CTF'[:2]:
            print(MENU2.decode())
            option = input('option >')
            if option == 'F':
                cip = self.enc_flag()
                print('Encrypted Flag: ' + hex(cip))

            elif option == 'G':
                dp,dq = self.get_dp_dq()
                print(f'dp,dq:{[dp,dq]}')

            elif option == 'T':
                self.time()

            else:
                break

if __name__ == "__main__":
    d3sys = D3_SYS()
    d3sys.handle()