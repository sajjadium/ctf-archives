from Crypto.Util.number import getStrongPrime, getPrime, GCD
import datetime


def encrypt(block, f, g, time):
    for c in time:
        if c == '1':
            block = f(block)
        elif c == '0':
            block = g(block)
    return block


def distribute_keys(block, f, g, start, end, so_far=''):
    if all(c == '0' for c in start) and all(c == '1' for c in end):
        print(so_far)
        print(hex(encrypt(block, f, g, so_far)))
        return
    if start[0] == end[0]:
        distribute_keys(block, f, g, start[1:], end[1:], so_far + start[0])
    else:
        distribute_keys(block, f, g, start[1:], '1' * len(end[1:]), so_far + '0')
        distribute_keys(block, f, g, '0' * len(start[1:]), end[1:], so_far + '1')
        return


def time_to_str(time):
    return ('0' * 64 + bin(int(time * 1000000))[2:])[-64:]


def pair_to_str(start, end):
    return ('0' * 64 + bin(int(start * 1000000))[2:])[-64:], ('0' * 64 + bin(int(end * 1000000) - 1)[2:])[-64:]


p = getStrongPrime(512)
q = getStrongPrime(512)
n = p * q
phi = (p - 1) * (q - 1)
now = time_to_str(datetime.datetime.now().timestamp())
while True:
    fe = getPrime(64)
    ge = getPrime(64)
    if GCD(phi, fe) == 1 and GCD(phi, ge) == 1:
        break
print(f'n={hex(n)}')
print(f'fe={hex(fe)}')
print(f'ge={hex(ge)}')
print(f'now={now}')
master_key = getStrongPrime(1024)


def f(block):
    return pow(block, fe, n)


def g(block):
    return pow(block, ge, n)


start, end = pair_to_str(datetime.datetime.strptime("1990", "%Y").timestamp(),
                         datetime.datetime.strptime("2020", "%Y").timestamp())
print(f'\nkeys: ')
distribute_keys(master_key, f, g, start, end)
flag = b'UMASS{REDACTED}'
flag_key = encrypt(master_key, f, g, now)
print()
print(f'flag={hex(int.from_bytes(flag) ^ flag_key)}')