#!/usr/bin/env python3

"""
Demo script that shows a setup of an OTP server with 2 OTP clients.

The seed of the OTP server is known by the administrator.
"""

import base64
import bip32utils
import mnemonic
import os
import struct
import sys
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization

from enum import IntEnum

from speculos.client import ApduException, SpeculosClient

SERVER_SEED = "lake essence common federal aisle amazing spend danger suspect barely verb try"
CLIENT1_SEED = "wire solve theme picnic matter aunt light volcano time bright produce verify"
CLIENT2_SEED = "entire dove rug stage garbage three elevator pair peace scrub convince monitor"


class Cmd(IntEnum):
    GET_PUBKEY = 0x00
    REGISTER_DEVICE = 0x01
    GET_REGISTERED_DEVICE_PUBKEY = 0x02
    ENCRYPT_OTP = 0x03
    DECRYPT_OTP = 0x04


def get_private_key_(mnemonic_words, path):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)

    bip32_child_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    for n in path:
        bip32_child_key_obj = bip32_child_key_obj.ChildKey(n)

    infos = {
        'mnemonic_words': mnemonic_words,
        'addr': bip32_child_key_obj.Address(),
        'publickey': bip32_child_key_obj.PublicKey().hex(),
        'privatekey': bip32_child_key_obj.WalletImportFormat(),
    }

    return bip32_child_key_obj.PrivateKey()


def get_private_key(seed):
    H = bip32utils.BIP32_HARDEN
    path = [ H | 13, H | 37, H | 0, 0, 0 ]
    private_bytes = get_private_key_(seed, path)
    private_value = int.from_bytes(private_bytes, "big")
    private_key = ec.derive_private_key(private_value, ec.SECP256K1(), default_backend())
    return private_key


def get_pubkey(peer):
    data = peer.apdu_exchange(0, Cmd.GET_PUBKEY, b"")
    return data


def get_encrypted_otp(server, n):
    epoch = int(time.time() / 30)
    payload = n.to_bytes(4, "little")
    payload += struct.pack('>q', epoch)
    data = server.apdu_exchange(0, Cmd.ENCRYPT_OTP, payload)
    return data


def register_device(server, client):
    private_key = get_private_key(SERVER_SEED)

    pubkey = get_pubkey(client)
    pubkey = pubkey.rjust(65, b"\x00")
    assert len(pubkey) == 65

    signature = private_key.sign(pubkey, ec.ECDSA(hashes.SHA256()))
    assert len(signature) <= 73

    print(f"[*] registering client with pubkey {pubkey.hex()}")
    payload = pubkey + signature.ljust(73, b"\x00") + len(signature).to_bytes(4, "little")
    data = server.apdu_exchange(0, Cmd.REGISTER_DEVICE, payload)


def decrypt_otp(server, client, data):
    pubkey = get_pubkey(server)
    assert len(data) == 32

    payload = pubkey.rjust(65, b"\x00") + data
    return client.apdu_exchange(0, Cmd.DECRYPT_OTP, payload)


if __name__ == "__main__":
    # run the OTP server
    with SpeculosClient("bin/app-server.elf", ["--seed", SERVER_SEED]) as server:

        # run 2 OTP clients
        with SpeculosClient("bin/app-client.elf", ["--seed", CLIENT1_SEED, "--api-port", "7000", "--apdu-port", "7001"], api_url="http://127.0.0.1:7000") as client1:
            with SpeculosClient("bin/app-client.elf", ["--seed", CLIENT2_SEED, "--api-port", "7002", "--apdu-port", "7003"], api_url="http://127.0.0.1:7002") as client2:

                # register the client devices on the server
                register_device(server, client1)
                register_device(server, client2)

                for i, client in enumerate([client1, client2]):
                    # ask the server for an OTP for the client i
                    encrypted_otp = get_encrypted_otp(server, i)
                    print(f"[*] encrypted OTP: {encrypted_otp.hex()}")

                    # decrypt it
                    otp = decrypt_otp(server, client, encrypted_otp)
                    otp = otp.replace(b"\x00", b'').decode("ascii")
                    print(f"[*] OTP: {otp}")
