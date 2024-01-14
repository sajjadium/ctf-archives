import ast
import threading
from exportcipher import *
try:
    from flag import FLAG
except:
    FLAG = "test{FLAG}"

MAX_COUNT = 100
TIMEOUT = 120 # seconds

def input_bytes(display_msg):
    m = input(display_msg)
    try:
        m = ast.literal_eval(m)
    except:
        # might not be valid str or bytes literal but could still be valid input, so just encode it
        pass
    if isinstance(m, str):
        m = m.encode()
    assert isinstance(m, bytes)
    return m

def timeout_handler():
    print("Time is up, you can throw out your work as the key changed.")
    exit()

if __name__ == "__main__":
    print("Initializing Export Grade Cipher...")
    key = int.from_bytes(os.urandom(5))
    cipher = ExportGradeCipher(key)
    print("You may choose up to {} plaintext messages to encrypt.".format(MAX_COUNT))
    print("Recover the 40-bit key to get the flag.")
    print("You have {} seconds.".format(TIMEOUT))
    # enough time to crack a 40 bit key with the compute resources of a government
    threading.Timer(TIMEOUT, timeout_handler).start()
    
    i = 0
    while i < MAX_COUNT:
        pt = input_bytes("[MSG {}] plaintext: ".format(i))
        if not pt:
            break
        if len(pt) > 512:
            # don't allow excessively long messages
            print("Message Too Long!")
            continue
        nonce = os.urandom(256)
        cipher.init_with_nonce(nonce)
        ct = cipher.encrypt(pt)
        print("[MSG {}] nonce: {}".format(i, nonce))
        print("[MSG {}] ciphertext: {}".format(i, ct))
        # sanity check decryption
        cipher.init_with_nonce(nonce)
        assert pt == cipher.decrypt(ct)
        i += 1
    recovered_key = ast.literal_eval(input("Recovered Key: "))
    assert isinstance(recovered_key, int)
    if recovered_key == key:
        print("That is the key! Here is the flag: {}".format(FLAG))
    else:
        print("Wrong!")