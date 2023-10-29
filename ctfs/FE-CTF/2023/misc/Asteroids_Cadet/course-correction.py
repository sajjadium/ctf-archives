#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import AES

WARP_COORDINATES = b'00000000-0000-0000-0000-000000000000'

HOST = args.get('HOST', 'localhost')
PORT = int(args.get('PORT', 1337))

sock = remote(HOST, PORT)

def course_correction(asteroids):
    '''We need to make this function run faster, sir'''
    size = int((len(asteroids)*8)**(1/3))
    for n in iters.count(1):
        for directions in iters.product('WASDQE', repeat=n):
            x = y = z = size // 2
            for m in iters.cycle(directions):
                match m:
                    case 'W': y += 1
                    case 'A': x -= 1
                    case 'S': y -= 1
                    case 'D': x += 1
                    case 'Q': z -= 1
                    case 'E': z += 1
                if x < 0 or x >= size or \
                   y < 0 or y >= size or \
                   z < 0 or z >= size:
                    return ''.join(directions)
                if x == y == z == size // 2:
                    break
                i, j = divmod(x + (y + z * size) * size, 8)
                if asteroids[i] & 1<<j:
                    break

def asteroids():
    while True:
        for _ in range(5):
            print(sock.recvline().decode(), end='')

        numb = sock.u32()
        data = sock.recvn(numb)

        sock.sendlineafter(b'Ready, captain?', b'Alright let\'s go in')
        key = sock.recvn(32)
        print(sock.recvline().decode(), end='')

        aes = AES.new(key, AES.MODE_CTR, nonce=b'')
        asteroids = aes.decrypt(data)

        course = course_correction(asteroids)
        print(f'Correcting course: {course}')
        sock.sendlineafter(b'Course correction> ', course.encode())
        print()

if __name__ == '__main__':
    try:
        sock.sendlineafter(b'Warp coordinates> ', WARP_COORDINATES)
        asteroids()
    except EOFError:
        print('its_been_an_honor.gif')
