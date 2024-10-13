import os

flag = open('flag.txt','r').read()
assert flag.startswith('TCP1P{') and flag.endswith('}')
flag = flag[6:-1]
assert len(flag) == 32

class Shiftgner:
    def __init__(self, mask):
        self.mask = int.from_bytes(mask, byteorder='big')

    def next(self):
        c = self.state & self.mask
        x = 0
        while c:
            x ^= c & 1
            c >>= 1
        self.state = ((self.state << 1) ^ x) & 2**256-1
        return x
    
    def sign(self, msg):
        self.state = msg
        op  = self.next()
        for i in range(255):
            op <<= 1
            op ^= self.next()
        op ^= msg
        return hex(op)

    def verify(self, msg, sig):
        return self.sign(msg) == sig

mask = os.urandom(32)
signer = Shiftgner(mask)

while True:
    print('1. Sign')
    print('2. Verify')
    print('3. Get Flag')
    print('4. Exit')
    op = int(input('> '))
    if op == 1:
        msg = int(input('Message (hex): '), 16)
        print('Signature:', signer.sign(msg))
    elif op == 2:
        msg = int(input('Message (hex): '), 16)
        sig = input('Signature: ')
        if signer.verify(msg, sig):
            print('OK')
        else:
            print('Invalid')
    elif op == 3:
        print(signer.sign(int.from_bytes(flag.encode(), byteorder='big')))
    elif op == 4:
        exit()
    else:
        print('Invalid')