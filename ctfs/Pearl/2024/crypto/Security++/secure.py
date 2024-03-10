from flag import flag, key
from base64 import b64encode
from enc import encrypt_block, pad


def encrypt(data: bytes):
    pt = data + flag
    pt = pad(pt)
    block_count = len(pt) // 16
    encText = b''
    for i in range(block_count):
        if i % 2 == 0:
            encText += encrypt_block(pt[i * 16:i * 16 + 16], key[0:16])
        else:
            encText += encrypt_block(pt[i * 16:i * 16 + 16], key[16:])
    return encText


def main():
    while 1:
        msg = input("\nEnter plaintext: ").strip()
        res = encrypt(msg.encode())
        print(b64encode(res).decode())


if __name__ == '__main__':
    main()
