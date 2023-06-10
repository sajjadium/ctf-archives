import random
import os

FLAG_RESPONSE = b'Please keep this for me: ' + os.getenv('FLAG', 'GPNCTF{fake_flag}').encode()

def get_next_seed():
    return os.urandom(12)

def store_leaked_data(data):
    # store leaked data from remote for later processing
    
    return

def store_exec_status(status):
    # store or process exec result status
    
    return

def get_flag():
    return FLAG_RESPONSE

MAX_COMMANDS = 3
def get_scheduled_cmds(max_len):
    cmds = b''
    for _ in range(MAX_COMMANDS):
        if max_len > 0 and random.random() > 0.7:
            if max_len >= 16 and random.random() > 0.9:
                cmds += b'\x05\x0enc -lvnp 31337'
            cmds += bytes([random.randint(1, 4)])
        else:
            break
    return cmds
