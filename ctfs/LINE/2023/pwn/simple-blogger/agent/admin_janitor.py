from pwn import *
import struct, os, binascii

HOST = 'server'
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASS')
PORT = 13443
TIMEOUT = 3

def auth():
    payload = b'\x01\x02'
    payload += b'\x41'*16
    cred = '{0}:{1}'.format(ADMIN_USER, ADMIN_PASS)
    cred_len = len(cred)
    payload += struct.pack('>H', cred_len)
    payload += cred.encode('utf-8')
    print(payload)
    return payload

def extract_sess(auth_res):
    sess = auth_res[4:]
    return sess

def clear_db(sess):
    payload = b'\x01\x01'
    payload += sess
    payload += b'\x00\x04'
    payload += b'PING'
    return payload

def connect(payload):
    r = remote(HOST, PORT)
    r.send(payload)
    data = r.recvrepeat(TIMEOUT)
    r.close()
    return data

res = connect(auth())
extracted_sess = extract_sess(res)
clear_res = connect(clear_db(extracted_sess))
print(binascii.hexlify(clear_res), end="")