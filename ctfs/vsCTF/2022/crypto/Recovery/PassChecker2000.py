# I coded this so that I wouldn't have to use a database!
from random import randint
from base64 import b64encode


def validate(password: str) -> bool:
    if len(password) != 49:
        return False

    key = ['vs'.join(str(randint(7, 9)) for _ in range(ord(i))) + 'vs' for i in password[::-2]]
    gate = [118, 140, 231, 176, 205, 480, 308, 872, 702, 820, 1034, 1176, 1339, 1232, 1605, 1792, 782, 810, 1197, 880,
            924, 1694, 2185, 2208, 2775]
    if [randint(a, b[0]) for a, b in enumerate(zip(gate, key), 1) if len(b[1]) != 3 * (b[0] + 7 * a) // a]:
        return False

    hammer = {str(a): password[a] + password[a + len(password) // 2] for a in range(1, len(password) // 2, 2)}
    block = b'c3MxLnRkMy57XzUuaE83LjVfOS5faDExLkxfMTMuR0gxNS5fTDE3LjNfMTkuMzEyMS5pMzIz'
    if b64encode(b'.'.join([((b + a).encode()) for a, b in hammer.items()])) != block:
        return False

    return True


if __name__ == "__main__":
    passwd = input('Please validate your ID using your password\n> ')
    if validate(passwd):
        print('Access Granted: You now have gained access to the View Source Flag Vault!')
    else:
        print('Access Denied :(')