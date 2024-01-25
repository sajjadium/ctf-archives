import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os
import sys

def tle_handler(*args):
    print('⏰')
    sys.exit(0)

class Quintessential_Quintuples:

    modes = (1, 2, 3, 5, 6) # I have no idea why MODE 4 doesn't exist, maybe it's because Yotsuba is the final winner in the comic i guess...

    def __init__(self):
        self.keys = dict(zip(self.modes, [hashlib.md5(os.urandom(3)).digest() for _ in self.modes]))
    
    def encrypt(self, m: bytes) -> bytes:
        c = pad(m, 16)
        ivs = []
        for mode in self.modes:
            if mode == AES.MODE_ECB:
                cipher = AES.new(key = self.keys[mode], mode = mode)
                c = cipher.encrypt(c)
            elif mode == AES.MODE_CBC or mode == AES.MODE_CFB or mode == AES.MODE_OFB:
                iv = os.urandom(16)
                cipher = AES.new(key = self.keys[mode], mode = mode, iv = iv)
                c = cipher.encrypt(c)
                ivs.append(iv)
            elif mode == AES.MODE_CTR:
                nonce = os.urandom(8)
                cipher = AES.new(key = self.keys[mode], mode = mode, nonce = nonce)
                c = cipher.encrypt(c)
                ivs.append(pad(nonce, 16))
            
        return b''.join(ivs) + c

    def decrypt(self, c: bytes) -> bytes:
        ivs, m = c[:16*4], c[16*4:]
        ivs = [ivs[i*16:(i+1)*16] for i in range(4)]
        for mode in self.modes[::-1]:
            if mode == AES.MODE_ECB:
                cipher = AES.new(key = self.keys[mode], mode = mode)
                m = cipher.decrypt(m)
            elif mode == AES.MODE_CBC or mode == AES.MODE_CFB or mode == AES.MODE_OFB:
                iv = ivs.pop()
                cipher = AES.new(key = self.keys[mode], mode = mode, iv = iv)
                m = cipher.decrypt(m)
            elif mode == AES.MODE_CTR:
                nonce = unpad(ivs.pop(), 16)
                cipher = AES.new(key = self.keys[mode], mode = mode, nonce = nonce)
                m = cipher.decrypt(m)

        return unpad(m, 16)


def main():

    signal.signal(signal.SIGALRM, tle_handler)
    signal.alarm(60)

    FLAG = os.environ.get('FLAG', 'firebird{***REDACTED***}').encode()
    QQ = Quintessential_Quintuples()

    commands = {'enc', 'dec', 'flag'}
    while True:
        command = input('🤖 ')
        if command not in commands:
            return print('😡')
        commands.remove(command)

        if command == 'enc':
            c = bytes.fromhex(input('💬 '))
            c = QQ.encrypt(c)
        elif command == 'dec':
            c = bytes.fromhex(input('💬 '))
            c = QQ.decrypt(c)
        elif command == 'flag':
            return print(f'🏁 {QQ.encrypt(FLAG).hex()}')

        print(f'🔑 {c.hex()}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('😒')