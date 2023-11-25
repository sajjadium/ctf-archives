#!/usr/bin/env python3

import ascon
import secrets
from secret import FLAG

BLOCK_SIZE = 16

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def split_blocks(message):
    return [message[i:i + BLOCK_SIZE] for i in range(0, len(message), BLOCK_SIZE)]


def mac_creation(key, message):
    assert len(message) % BLOCK_SIZE == 0
    message_blocks = split_blocks(message)
    enc_out = b"\x00" * BLOCK_SIZE
    for message in message_blocks:
        chaining_values = xor(message, enc_out)
        enc_out = ascon.encrypt(key, chaining_values, b'', b'')
    assert len(enc_out) == BLOCK_SIZE
    return enc_out


def pad_message(message):
    first_block_pad = len(message) % BLOCK_SIZE
    first_block_pad = 16 if first_block_pad == 0 else first_block_pad
    return  (first_block_pad.to_bytes() * (BLOCK_SIZE - first_block_pad)) + message


def encrypt(key,  message):
    assert len(message) % BLOCK_SIZE == 0
    message_blocks = split_blocks(message)

    assert len(message_blocks) < BLOCK_SIZE
    nonce = secrets.token_bytes(BLOCK_SIZE-1)

    cts = []
    for ctr, message in enumerate(message_blocks):
        cipher_input = nonce + (ctr+1).to_bytes(1, 'little')

        enc = ascon.encrypt(key, cipher_input, b'', b'')

        ct = xor(message, enc)
        cts.append(ct)
    return nonce, b''.join(cts)


def create_message_and_mac(key, message):
    padded_message = pad_message(message)
    nonce, ct = encrypt(key, padded_message)
    tag = mac_creation(key, padded_message)
    return nonce, ct, tag

if __name__ == "__main__":
    print("              Glacier Spirit\n\n")
    print("           ,                  /\.__      _.-\ ")
    print("          /~\,      __       /~    \   ./    \ ")
    print("        ,/  /_\   _/  \    ,/~,_.~''\ /_\_  /'\ ")
    print("       / \ /## \ / V#\/\  /~8#  # ## V8  #\/8 8\ ")
    print("     /~#'#'#''##V&#&# ##\/88#'#8# #' #\#&'##' ##\ ")
    print("    j# ##### #'#\&&'####/###&  #'#&## #&' #'#&#'#'\ ")
    print("   /#'#'#####'###'\&##'/&#'####'### # #&#&##'#'### \ ")
    print("  J#'###'#'#'#'####'\# #'##'#'##'#'#####&'## '#'&'##|\ ")
    
    key = secrets.token_bytes(BLOCK_SIZE)
    
    print("The spirit of the glacier gifts you a flag!\n")
    nonce, ct, tag = create_message_and_mac(key, FLAG)
    print(f"{nonce.hex()}, {ct.hex()}, {tag.hex()}")
    
    print("\nNow you can bring forth your own messages to be blessed by the spirit of the glacier!\n")
    for i in range(8):
        print(f"Offer your message:")
        user_msg = input()
        try:
            msg = bytes.fromhex(user_msg)
        except:
            print("The spirit of the glacier is displeased with the format of your message.")
            exit(0)
        nonce, ct, tag = create_message_and_mac(key, msg)
        print("The spirit of the glacier has blessed your message!\n")
        print(f"{nonce.hex()}, {ct.hex()}, {tag.hex()}")
    
    print("The spirit of the glacier has left you. You are alone once more.")