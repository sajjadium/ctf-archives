#!/usr/bin/python3 -u

import os, sys, random, subprocess, gmpy2
from io import BytesIO
from hashlib import sha3_256
from elftools.elf.elffile import ELFFile
from elftools.elf.constants import P_FLAGS

os.chdir(os.path.dirname(__file__))

def proof_of_work(sec = 10):
    # From 0CTF/TCTF 2021
    p = gmpy2.next_prime(random.getrandbits(512))
    q = gmpy2.next_prime(random.getrandbits(512))
    n = p*q
    c = 2900000
    t = c*sec + random.randint(0,c)
    print('Show me your computation:')
    print(f'2^(2^{t}) mod {n} = ?')
    print('Your answer: ', end='')
    try:
        sol = int(sys.stdin.readline())
        phi = (p-1)*(q-1)
        u = pow(2, t, phi)
        w = pow(2, u, n)
        if w == sol:
            print('Correct!')
            return True
        else:
            print('Wrong Answer!')
            exit()
    except ValueError:
        print('Invalid Input!')
        exit()

def check_bytes(data, b):
    p = -1
    while True:
        p = data.find(b, p+1)
        if p == -1:
            return True
        elif p & 0xfff == 0 or p & 0xfff == 0xfff:
            return False

def check_segments(elf):
    for seg in elf.iter_segments():
        if seg.header.p_filesz > 0x10000 or seg.header.p_memsz > 0x10000:
            print('Segment too large')
            return False
        elif seg.header.p_type == 'PT_INTERP' or seg.header.p_type == 'PT_DYNAMIC':
            print('No dynamic link')
            return False
        elif seg.header.p_type == 'PT_LOAD' and seg.header.p_flags & P_FLAGS.PF_W and seg.header.p_flags & P_FLAGS.PF_X:
            print('W^X')
            return False
        elif seg.header.p_type == 'PT_GNU_STACK' and seg.header.p_flags & P_FLAGS.PF_X:
            print('No executable stack')
            return False

    return True

def check_elf(data):
    if len(data) < 0x40:
        print('Incomplete ELF Header')
        return False

    if not data.startswith(b'\x7fELF\x02\x01\x01' + b'\x00'*9):
        print('Invalid ELF Magic')
        return False

    if b'\xcd\x80' in data or b'\x0f\x05' in data:
        print('Bad Instruction')
        return False

    if not check_bytes(data, b'\xcd') or not check_bytes(data, b'\x80') or not check_bytes(data, b'\x0f') or not check_bytes(data, b'\x05'):
        print('Bad Instruction')
        return False

    elf = ELFFile(BytesIO(data))
    if ((elf.header.e_type != 'ET_EXEC' and elf.header.e_type != 'ET_DYN')
        or elf.header.e_version != 'EV_CURRENT'
        or elf.header.e_ehsize != 0x40
        or elf.header.e_phoff != 0x40
        or elf.header.e_phnum <= 0
        or elf.header.e_phnum >= 100):
        print('Bad ELF Header')
        return False

    return check_segments(elf)

def main():
    try:
        size = int(input('Size of your ELF: '))
    except:
        print('Invalid size!')
        return
    if size <= 0 or size > 0x10000:
        print('Bad size!')
        return

    print('ELF File:')
    try:
        data = sys.stdin.buffer.read(size)
    except:
        print('Invalid file data')
        return
    if len(data) != size:
        print('Incomplete file data')
        return

    print('Received: %d bytes' % len(data))
    if check_elf(data):
        filename = sha3_256(data).hexdigest()
        print(f'File Hash: {filename}')
        path = f'./data/{filename}'
        if os.path.exists(path):
            os.unlink(path)
        open(path, 'wb').write(data)
        os.chmod(path, 0o555)
        try:
            p = subprocess.Popen(['docker', 'run', '-i', '--rm', '-v', f'{path}:/chroot/{filename}', 'tctf/launcher64:2023', filename], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.wait()
            print('Return status: %d' % p.returncode)
            if p.returncode == 137:
                print('Output:')
                sys.stdout.buffer.write(p.stdout.read())
                return
        except:
            print('Something went wrong!')

if __name__ == '__main__':
    if proof_of_work():
        main()
        print('Bye!')
