#!/usr/bin/env python3

import base64
import io
import os
import qrcode
import random
import secrets
import zlib

FLAG = os.getenv('FLAG', 'flag{fake_flag}')
SOULS = int(os.getenv('SOULS', '20'))
SHARDS = int(os.getenv('SHARDS', '17'))

BLOCK_FULL  = chr(9608)
BLOCK_UPPER = chr(9600)
BLOCK_LOWER = chr(9604)
BLOCK_EMPTY = chr(160)

def select_soul():
    return secrets.token_urlsafe(16)

def soul_code(data):
    code = qrcode.QRCode(
        border=0,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    code.add_data(data)
    code.make()
    return code

def code_atoms(code):
    size = len(code.modules)
    atoms = []
    for y in range(size):
        for x in range(size):
            atoms.append((x, y, code.modules[y][x]))
    return atoms, size

def atoms_to_text(size, atoms):
    buf = [False] * size**2
    for atom in atoms:
        x, y, is_set = atom
        buf[y * size + x] = is_set
    text = io.StringIO()
    for y in range(0, size, 2):
        for x in range(size):
            a = buf[y * size + x]
            b = buf[(y + 1) * size + x] if (y + 1) * size + x < len(buf) else False
            if a and b:
                text.write(BLOCK_FULL)
            elif a:
                text.write(BLOCK_UPPER)
            elif b:
                text.write(BLOCK_LOWER)
            else:
                text.write(BLOCK_EMPTY)
        text.write('\n')
    return text.getvalue().strip('\n')

def atoms_token(size, atoms):
    text = atoms_to_text(size, atoms)
    return base64.b64encode(zlib.compress(text.encode('utf-8'))).decode('utf-8')

def split_soul(soul, n):
    code = soul_code(soul)
    atoms, size = code_atoms(code)
    random.shuffle(atoms)
    atom_count = len(atoms)
    r = atom_count % n
    atoms_per_shard = atom_count // n
    shard_codes = []
    for i in range(0, atom_count - r, atoms_per_shard):
        shard_codes.append(atoms[i:i + atoms_per_shard])
    for i in range(r):
        shard_codes[i].append(atoms[-1 - i])
    return [atoms_token(size, shard_code) for shard_code in shard_codes]

def generate_challenge():
    soul = select_soul()
    shards = split_soul(soul, SHARDS)
    return soul, random.sample(shards, SHARDS - 1)

def main():
    print('👹 I am the Soul Splitter!')
    print(f'👹 If you can recover {SOULS} souls, I will tell you my secret.')
    for _ in range(SOULS):
        soul, shards = generate_challenge()
        print(f'👹 Here are {len(shards)} shards:')
        print('\n'.join(shards))
        recovered = input('👹 Recover the soul to prove you are worthy: ')
        if recovered != soul:
            print('👹 Wrong! You are unworthy. ' + soul)
            return
        print('👹 You got lucky with this one...')
    print('👹 You haven proven yourself! Here\'s my secret:')
    print(FLAG)

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
