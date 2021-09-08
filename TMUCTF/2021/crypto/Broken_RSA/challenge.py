from Crypto.Util.number import *

e = 65537

with open('n', 'rb') as f:
    n = int(f.read())

with open('secret', 'rb') as f:
    secret_msg = f.read()

pads = [b'\x04', b'\x02', b'\x00', b'\x01', b'\x03']

with open('out.txt', 'w') as f:
    for i in range(len(pads)):
        for j in range(len(pads)):
            msg = pads[j] * (i + 1) + b'TMUCTF' + pads[len(pads) - j - 1] * (i + 1)
            enc = pow(bytes_to_long(msg), e, n)
            f.write(str(enc) + '\n')

    enc = pow(bytes_to_long(secret_msg), e, n)
    f.write(str(enc))
