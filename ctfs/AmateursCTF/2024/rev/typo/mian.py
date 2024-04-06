import random as RrRrRrrrRrRRrrRRrRRrrRr
RrRrRrrrRrRRrrRRrRRrRrr = int('1665663c', 20)
RrRrRrrrRrRRrrRRrRRrrRr.seed(RrRrRrrrRrRRrrRRrRRrRrr)
arRRrrRRrRRrRRRrRrRRrRr = bytearray(open('flag.txt', 'rb').read())
arRRrrRrrRRrRRRrRrRRrRr = '\r'r'\r''r''\\r'r'\\r\r'r'r''r''\\r'r'r\r'r'r\\r''r'r'r''r''\\r'r'\\r\r'r'r''r''\\r'r'rr\r''\r''r''r\\'r'\r''\r''r\\\r'r'r\r''\rr'
arRRrrRRrRRrRrRrRrRRrRr = [
    b'arRRrrRRrRRrRRrRr',
    b'aRrRrrRRrRr',
    b'arRRrrRRrRRrRr',
    b'arRRrRrRRrRr',
    b'arRRrRRrRrrRRrRR'
    b'arRRrrRRrRRRrRRrRr',
    b'arRRrrRRrRRRrRr',
    b'arRRrrRRrRRRrRr'
    b'arRrRrRrRRRrrRrrrR',
]
arRRRrRRrRRrRRRrRrRRrRr = lambda aRrRrRrrrRrRRrrRRrRrrRr: bytearray([arRrrrRRrRRrRRRrRrRrrRr + 1 for arRrrrRRrRRrRRRrRrRrrRr in aRrRrRrrrRrRRrrRRrRrrRr])
arRRrrRRrRRrRRRrRrRrrRr = lambda aRrRrRrrrRrRRrrRRrRrrRr: bytearray([arRrrrRRrRRrRRRrRrRrrRr - 1 for arRrrrRRrRRrRRRrRrRrrRr in aRrRrRrrrRrRRrrRRrRrrRr])
def arRRrrRRrRRrRrRRrRrrRrRr(hex):
    for id in range(0, len(hex) - 1, 2):
        hex[id], hex[id + 1] = hex[id + 1], hex[id]
    for list in range(1, len(hex) - 1, 2):
        hex[list], hex[list + 1] = hex[list + 1], hex[list]
    return hex
arRRRRRRrRRrRRRrRrRrrRr = [arRRrrRRrRRrRrRRrRrrRrRr, arRRRrRRrRRrRRRrRrRRrRr, arRRrrRRrRRrRRRrRrRrrRr]
arRRRRRRrRRrRRRrRrRrrRr = [RrRrRrrrRrRRrrRRrRRrrRr.choice(arRRRRRRrRRrRRRrRrRrrRr) for arRrrrRRrRRrRRRrRrRrrRr in range(128)]
def RrRrRrrrRrRRrrRRrRRrrRr(arr, ar):
    for r in ar:
        arr = arRRRRRRrRRrRRRrRrRrrRr[r](arr)
    return arr
def arRRrrRRrRRrRrRRrRrrRrRr(arr, ar):
    ar = int(ar.hex(), 17)
    for r in arr:
        ar += int(r, 35)
    return bytes.fromhex(hex(ar)[2:])
arrRRrrrrRRrRRRrRrRRRRr = RrRrRrrrRrRRrrRRrRRrrRr(arRRrrRRrRRrRRRrRrRRrRr, arRRrrRrrRRrRRRrRrRRrRr.encode())
arrRRrrrrRRrRRRrRrRRRRr = arRRrrRRrRRrRrRRrRrrRrRr(arRRrrRRrRRrRrRrRrRRrRr, arrRRrrrrRRrRRRrRrRRRRr)
print(arrRRrrrrRRrRRRrRrRRRRr.hex())