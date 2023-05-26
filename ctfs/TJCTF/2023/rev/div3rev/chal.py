def op1(b):
    for i in range(len(b)):
        b[i] += 8*(((b[i] % 10)*b[i]+75) & 1)
        cur = 1
        for j in range(420):
            cur *= (b[i]+j) % 420
    return b


def op2(b):
    for i in range(len(b)):
        for j in range(100):
            b[i] = b[i] ^ 69
        b[i] += 12
    return b


def op3(b):
    for i in range(len(b)):
        b[i] = ((b[i] % 2) << 7)+(b[i]//2)
    return b


def recur(b):
    if len(b) == 1:
        return b
    assert len(b) % 3 == 0
    a = len(b)
    return op1(recur(b[0:a//3]))+op2(recur(b[a//3:2*a//3]))+op3(recur(b[2*a//3:]))


flag = open("flag.txt", "r").read()
flag = flag[:-1]
b = bytearray()
b.extend(map(ord, flag))
res = recur(b)
if res == b'\x8c\x86\xb1\x90\x86\xc9=\xbe\x9b\x80\x87\xca\x86\x8dKJ\xc4e?\xbc\xdbC\xbe!Y \xaf':
    print("correct")
else:
    print("oopsies")
