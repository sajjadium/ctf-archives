#!/usr/bin/env python3

import json
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from secret import FLAG, CMAC_KEY, PUBKEY_TAG, try_read_cmac_key


def mac(msg):
    cmac = CMAC.new(CMAC_KEY, ciphermod=AES)
    cmac.oid = '2.16.840.1.101.3.4.2.42'
    cmac.update(msg)
    return cmac


def do_update():
    update = json.loads(input('update package: '))
    n_bytes = bytes.fromhex(update['pubkey'])
    signature_bytes = bytes.fromhex(update['signature'])
    payload_bytes = bytes.fromhex(update['payload'])

    key_tag = mac(n_bytes).digest()
    if key_tag != PUBKEY_TAG:
        print('verification failed')
        return

    n = int.from_bytes(n_bytes, 'big')
    e = 0x10001
    pubkey = RSA.construct((n, e))
    verifier = pkcs1_15.new(pubkey)

    h = mac(payload_bytes)
    signature = signature_bytes

    try:
        verifier.verify(h, signature)
    except:
        print('verification failed')
        return
    print('signature correct')

    if payload_bytes == b'Gimmie a flag, pretty please.':
        print(FLAG)

    print('update succesfull')


def main():
    while True:
        print('1. try to read cmac key')
        print('2. do an update')
        choice = int(input('your choice: '))
        if choice == 1:
            print(try_read_cmac_key())
        elif choice == 2:
            do_update()
        else: break


main()
