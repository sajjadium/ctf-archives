from Crypto.Util import number

flag = b"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def convert(msg):
    msg = msg ^ msg >> x
    msg = msg ^ msg << 13 & 275128763
    msg = msg ^ msg << 20 & 2186268085
    msg = msg ^ msg >> 14
    return msg

def transform(message):
    assert len(message) % 4 == 0
    new_message = b''
    for i in range(int(len(message) / 4)):
        block = message[i * 4 : i * 4 +4]
        block = number.bytes_to_long(block)
        block = convert(block)
        block = number.long_to_bytes(block, 4)
        new_message += block
    return new_message

c = transform(flag[6:-1]).hex()
print('c =', c)
'''
c = e34a707c5c1970cc6375181577612a4ed07a2c3e3f441d6af808a8acd4310b89bd7e2bb9
'''
