import binascii
import random

flag = ""

fl = int(binascii.hexlify(flag), 16)

p = 1 << 1024
b = random.randint(0, p) | 1
s = random.randint(0, p)
x = pow(b, s, p)

print('p: {}'.format(p))
print('b: {}'.format(b))
print('x: {}'.format(x))

y = int(input('y: '))

z = pow(y, s, p)
Message = fl ^ z
print('Message: {}'.format(Message))
